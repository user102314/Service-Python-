from flask import Blueprint, jsonify
import os
import pyttsx3
from src.services.text_processor import TextProcessor
from src.services.n8n_client import N8NClient
from src.services.response_processor import ResponseProcessor
from src.services.orchestrator import Orchestrator
from src.services.azure_speech_service import AzureSpeechService

# On crée un "Blueprint" pour ce module
robot_bp = Blueprint('robot_controller', __name__)

# Initialisation du système
speech_svc = AzureSpeechService()
text_proc = TextProcessor()
n8n_cli = N8NClient(os.getenv("N8N_WEBHOOK_URL"))
resp_proc = ResponseProcessor()
robot_system = Orchestrator(speech_svc, text_proc, n8n_cli, resp_proc)


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.say(text)
    engine.runAndWait()


@robot_bp.route('/api/getReponceFromRobot', methods=['POST'])
def get_reponce_from_robot():
    try:
        # Lancement du pipeline IA
        result = robot_system.run("input_audio.wav")

        # Parole du robot
        speak(result.get('answer'))

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500