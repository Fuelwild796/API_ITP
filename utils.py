import numpy as np
from fastapi import HTTPException, Depends
from starlette.status import HTTP_403_FORBIDDEN
from fastapi.security.api_key import APIKeyHeader
import os

labels = [
    'Satisfação',
    'Frustração',
    'Confusão',
    'Urgência/Pressão',
    'Raiva/Irritação',
    'Neutro'
]

API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key")

def get_api_key(api_key: str = Depends(api_key_header)):
    if API_KEY is None or api_key != API_KEY:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid API Key")

def predict_sentiment(text, infer, tokenizer):
    import tensorflow as tf
    inputs = tokenizer(
        text,
        return_tensors="tf",
        truncation=True,
        padding="max_length",
        max_length=64
    )
    input_ids = tf.cast(inputs["input_ids"], tf.float32)
    attention_mask = tf.cast(inputs["attention_mask"], tf.float32)
    if input_ids.shape[0] < 16:
        pad = 16 - input_ids.shape[0]
        input_ids = tf.pad(input_ids, [[0, pad], [0, 0]])
        attention_mask = tf.pad(attention_mask, [[0, pad], [0, 0]])
    outputs = infer(
        inputs=input_ids,
        inputs_1=attention_mask
    )
    logits = list(outputs.values())[0].numpy()
    pred = np.argmax(logits[0])
    return labels[pred]