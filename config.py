import os
from dotenv import load_dotenv

load_dotenv()

class config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    MODEL_NAME = "llama-3.3-70b-versatile"
    MAX_TOKENS = 720
    TEMPERATURE = 0.7

    MAX_RETRIES= 3
    TIMEOUT = 30

    KNOWLWDGE_BASE_DIR = "knowledge_base"
    CHROMA_DIR = "chroma_db"

    CONFIDENCE_THRESHOLD = 0.7

    MAX_ATTEMPTS_BEFORE_ESCALATION = 3
    SENSITIVE_KEYWORDS = ['lawsuit','lawyer','legal','assault']

config = config()