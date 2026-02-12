import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

#API Configuration

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise EnvironmentError(
        "GEMINI_API_KEY not found. Please set it in your environment or .env file."
    )

#Path Configuration

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
CHROMA_DB_DIR = DATA_DIR / "chroma_db"

DATA_DIR.mkdir(exist_ok=True)
CHROMA_DB_DIR.mkdir(exist_ok=True)

#Memory Configuration

#Number of memories to retrieve per interaction
MEMORY_TOP_K = 5

#Importance threshold to consider memory relevant
MEMORY_IMPORTANCE_THRESHOLD = 0.5

#Number of interactions after which summarization runs
MEMORY_SUMMARIZATION_INTERVAL = 10

#Gossip only spreads if importance exceeds this
GOSSIP_IMPORTANCE_THRESHOLD = 0.4

#NPC Behavior Limits

RELATIONSHIP_MIN = -100
RELATIONSHIP_MAX = 100

#LLM Configuration

LLM_MODEL_NAME = "gemini-2.5-flash"
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 1024

#Embeddings Configuration

#Keep embeddings consistent across the project
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

#Debug / Dev Settings

DEBUG = True