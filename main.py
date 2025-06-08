import os
import zipfile
import logging
from fastapi import FastAPI
from routers import sentiment
from utils import get_api_key, labels, predict_sentiment
import tensorflow as tf
from transformers import BertTokenizerFast
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()
API_KEY = os.getenv("API_KEY")
MODEL_URL = os.getenv("MODEL_URL")
ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN", "http://localhost")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_ZIP_PATH = os.path.join(BASE_DIR, "modelo_bertimbau.zip")
MODEL_DIR = os.path.join(BASE_DIR, "bert_saved_model")
TOKENIZER_DIR = os.path.join(BASE_DIR, "bert_tokenizer")


if not API_KEY or not MODEL_URL:
    logger.error("API_KEY ou MODEL_URL não definida no .env.")
    raise RuntimeError("API_KEY ou MODEL_URL não definida no .env.")

logger.info(f"API_KEY carregada: {API_KEY}")

# Configuração de CORS
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.path.exists(MODEL_DIR) or not os.path.exists(TOKENIZER_DIR):
    try:
        import gdown
        logger.info("Baixando modelo e tokenizer...")
        gdown.download(MODEL_URL, MODEL_ZIP_PATH, quiet=False)
        with zipfile.ZipFile(MODEL_ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(BASE_DIR)  # Extrai sempre na pasta do main.py
        os.remove(MODEL_ZIP_PATH)
        logger.info("Modelo e tokenizer baixados e extraídos com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao baixar/extrair modelo: {e}")
        raise RuntimeError(f"Erro ao baixar/extrair modelo: {e}")


try:
    model = tf.saved_model.load(MODEL_DIR)
    infer = model.signatures["serving_default"]
    tokenizer = BertTokenizerFast.from_pretrained(TOKENIZER_DIR)
    app.state.infer = infer
    app.state.tokenizer = tokenizer
    logger.info("Modelo e tokenizer carregados com sucesso.")
except Exception as e:
    logger.error(f"Erro ao carregar modelo/tokenizer: {e}")
    raise RuntimeError(f"Erro ao carregar modelo/tokenizer: {e}")

class AcaoCreate(BaseModel):
    descricao: str = Field(..., min_length=1)
    event_id: int

class AcaoResposta(AcaoCreate):
    sentimento: str
    data_acao: datetime


app.include_router(sentiment.router)

@app.get("/health/")
def health():
    """Endpoint de verificação de saúde da API."""
    return {"status": "ok"}