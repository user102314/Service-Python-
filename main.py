import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import mysql.connector

# Import de tes services existants
from src.services.text_processor import TextProcessor
from src.services.n8n_client import N8NClient
from src.services.response_processor import ResponseProcessor
from src.services.orchestrator import Orchestrator
from src.services.speech_service import MockAzureSpeechService  # On garde la simulation
import pyttsx3

load_dotenv()

app = Flask(__name__)
CORS(app)  # Autorise les requêtes depuis un front-end

# Configuration MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',  # À adapter
    'password': '',  # À adapter
    'database': 'pfe'
}

# Initialisation du pipeline Robot
speech_svc = MockAzureSpeechService()
text_proc = TextProcessor()
n8n_cli = N8NClient(os.getenv("N8N_WEBHOOK_URL"))
resp_proc = ResponseProcessor()
robot_system = Orchestrator(speech_svc, text_proc, n8n_cli, resp_proc)


def speak(text):
    """Le robot parle sur le serveur"""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# --- ENDPOINT 1 : Obtenir réponse du Robot ---
@app.route('/api/getReponceFromRobot', methods=['POST'])
def get_reponce_from_robot():
    try:
        # On exécute le pipeline (ici via simulation console ou data JSON)
        result = robot_system.run("input_audio.wav")

        # Le robot parle
        speak(result.get('answer'))

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- ENDPOINT 2 : Afficher toutes les notes ---
@app.route('/api/notes', methods=['GET'])
def get_all_notes():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM note")
        notes = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(notes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- ENDPOINT 3 : Modifier l'état d'une note (Set False) ---
@app.route('/api/notes/<int:note_id>/desactiver', methods=['PUT'])
def update_note_etat(note_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # On met l'état à False (0 en MySQL) pour l'ID donné
        query = "UPDATE note SET etat = 0 WHERE id = %s"
        cursor.execute(query, (note_id,))
        conn.commit()

        count = cursor.rowcount
        cursor.close()
        conn.close()

        if count == 0:
            return jsonify({"message": "Note non trouvée"}), 404

        return jsonify({"message": f"État de la note {note_id} mis à False"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)