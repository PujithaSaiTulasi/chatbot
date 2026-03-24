from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
load_dotenv()
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OLLAMA_URL = "http://localhost:11434/api/generate" - Use this if running FastAPI locally and Ollama in Docker | both locally as well
# OLLAMA_URL = "http://host.docker.internal:11434/api/generate" - Use this if running Ollama locally and FastAPI in Docker
OLLAMA_URL = "http://ollama:11434/api/generate" # - Use this if running FastAPI in Docker and Ollama in another container named "ollama" (with same network)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": os.getenv("MODEL_NAME"),
            "prompt": req.message,
            "stream": False
        }
    )

    try:
        data = response.json()
    except Exception:
        return {"error": "Invalid JSON from Ollama"}

    # DEBUG: print full response
    print("Ollama response:", data)

    if "response" not in data:
        return {
            "error": "No response from model",
            "details": data
        }

    return {
        "response": data["response"]
    }
