# LLM Chatbot Deployment Guide

Four ways to run the Ollama server and FastAPI backend — locally, in Docker, or a mix of both.

---

## 1. Run Both Locally

**Project Structure**
```
chatbot/
│
├── venv/
├── main.py
├── index.html
├── requirements.txt
└── .env
```

**Setup**
```bash
cd Desktop/chatbot
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn requests python-dotenv
pip freeze > requirements.txt
```

**Environment Variable**
```
OLLAMA_URL = "http://localhost:11434/api/generate"
```

**Run**

| Terminal | Command |
|----------|---------|
| Terminal 1 | `uvicorn main:app --reload` |
| Terminal 2 | `ollama run mistral` |

Then open `index.html` in your browser.

---

## 2. Ollama Locally + Backend on Docker

**Project Structure**
```
chatbot/
│
├── main.py
├── requirements.txt
├── Dockerfile
├── index.html
└── .dockerignore
```

**Environment Variable**
```
OLLAMA_URL = "http://host.docker.internal:11434/api/generate"
```
> `host.docker.internal` allows the Docker container to reach services running on your local machine.

**Run**

| Terminal | Command |
|----------|---------|
| Terminal 1 | `docker build -t chatbot .` then `docker run -p 8000:8000 chatbot` |
| Terminal 2 | `ollama run mistral` |

Then open `index.html` in your browser.

---

## 3. Ollama on Docker + Backend Locally

**Environment Variable**
```
OLLAMA_URL = "http://localhost:11434/api/generate"
```
> Since the backend runs locally (not inside a container), `localhost` correctly points to your machine where Ollama's port is exposed.

**Run**

| Terminal | Command |
|----------|---------|
| Terminal 1 | `uvicorn main:app --reload` |
| Terminal 2 | `docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama` |
| Terminal 2 | `docker exec -it ollama ollama pull tinyllama` |

---

## 4. Run Both on Docker

**Environment Variable**
```
OLLAMA_URL = "http://ollama:11434/api/generate"
```
> When both services run in separate containers on the same Docker network, use the **container name** as the hostname instead of `localhost`.

**Run**
```bash
# Create a shared network
docker network create mynet

# Connect both containers to the network
docker network connect mynet <ollama_container_name>
docker network connect mynet <app_container_name>

# Restart the app container to apply network changes
docker restart <app_container_name>
```

---

## Quick Reference

| Scenario | `OLLAMA_URL` Host |
|---|---|
| Both local | `localhost` |
| Ollama local, Backend in Docker | `host.docker.internal` |
| Ollama in Docker, Backend local | `localhost` |
| Both in Docker (same network) | `ollama` *(container name)* |