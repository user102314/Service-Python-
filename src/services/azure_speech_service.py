import azure.cognitiveservices.speech as speechsdk
from src.utils.exceptions import TranscriptionError
from src.utils.logger import logger


class AzureSpeechService:
    def __init__(self, key, region):
        self.config = speechsdk.SpeechConfig(subscription=key, region=region)
        self.config.speech_recognition_language = "fr-FR"

    def transcribe(self, audio_path: str) -> str:
        logger.info(f"Début transcription : {audio_path}")
        audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
        recognizer = speechsdk.SpeechRecognizer(speech_config=self.config, audio_config=audio_config)

        result = recognizer.recognize_once_async().get()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            logger.info("Transcription réussie.")
            return result.text

        logger.error(f"Échec transcription : {result.reason}")
        raise TranscriptionError(f"Azure Speech Error: {result.reason}")