import re

class TextProcessor:
    def clean(self, text: str) -> str:
        # Nettoyage basique : suppression des espaces multiples et mise en minuscule
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        return text

    def enrich(self, text: str) -> dict:
        # Analyse simple pour ajouter des métadonnées
        return {
            "raw_content": text,
            "word_count": len(text.split()),
            "language": "fr"
        }