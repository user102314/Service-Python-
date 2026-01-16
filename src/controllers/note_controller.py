from flask import Blueprint, jsonify, request
import mysql.connector

note_bp = Blueprint('note_controller', __name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'pfe'
}


@note_bp.route('/api/notes', methods=['GET'])
def get_all_notes():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, note, etat FROM note")
        notes = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(notes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@note_bp.route('/api/notes/<int:note_id>/desactiver', methods=['PUT'])
def desactiver_note(note_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # Mise à jour de l'état à False (0)
        cursor.execute("UPDATE note SET etat = 0 WHERE id = %s", (note_id,))
        conn.commit()

        status = "success" if cursor.rowcount > 0 else "not_found"
        cursor.close()
        conn.close()

        if status == "not_found":
            return jsonify({"message": "Note non trouvée"}), 404
        return jsonify({"message": f"Note {note_id} désactivée avec succès"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500