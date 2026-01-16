import json
from src.utils.logger import logger


class ResponseProcessor:
    def process(self, n8n_response: dict) -> dict:
        # Si n8n renvoie une liste, on prend le premier élément
        if isinstance(n8n_response, list) and len(n8n_response) > 0:
            n8n_response = n8n_response[0]

        # On récupère la clé 'reponse_finale' que nous avons vue dans vos logs
        raw_data = n8n_response.get("reponse_finale", "")

        answer = "Désolé, je n'ai pas pu extraire la réponse."

        try:
            # On tente de décoder la chaîne JSON contenue dans 'reponse_finale'
            parsed = json.loads(raw_data)
            answer = parsed.get("output", raw_data)
        except (json.JSONDecodeError, TypeError):
            # Si ce n'est pas du JSON, on cherche les clés standards ou on prend le brut
            answer = n8n_response.get("output") or n8n_response.get("text") or raw_data

        return {
            "status": "success",
            "answer": answer
        }