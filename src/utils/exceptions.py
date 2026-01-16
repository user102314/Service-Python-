class PFEBaseException(Exception):
    """Exception de base pour le projet"""
    pass

class TranscriptionError(PFEBaseException):
    """Erreur lors de la transcription Azure"""
    pass

class N8NCommunicationError(PFEBaseException):
    """Erreur lors de l'appel au workflow N8N"""
    pass