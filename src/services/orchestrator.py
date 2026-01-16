from src.utils.logger import logger


class Orchestrator:
    def __init__(self, speech_svc, text_proc, n8n_cli, resp_proc):
        self.speech_svc = speech_svc
        self.text_proc = text_proc
        self.n8n_cli = n8n_cli
        self.resp_proc = resp_proc

    def run(self, audio_file: str):
        logger.info("--- Démarrage du pipeline ---")

        # 1. Transcription
        text = self.speech_svc.transcribe(audio_file)

        # 2. Traitement
        cleaned_text = self.text_proc.clean(text)
        payload = self.text_proc.enrich(cleaned_text)

        # 3. N8N
        n8n_raw = self.n8n_cli.send_payload(payload)

        # 4. Finalisation
        final_result = self.resp_proc.process(n8n_raw)

        logger.info("--- Pipeline terminé avec succès ---")
        return final_result