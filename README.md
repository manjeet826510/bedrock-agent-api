# Bedrock Agent API

A production-ready REST API built with FastAPI to interact with an Amazon Bedrock Agent **with memory support**.  
This service enables stateful conversations by maintaining session context while communicating with Bedrock agents.

🚀 **Live API (Deployed):**  
https://bedrock-agent-api.onrender.com/docs

---

## 🔥 Key Features

- FastAPI-based REST API
- Amazon Bedrock Agent integration
- 🧠 **Stateful conversations using agent memory**
- Session-aware request handling
- Swagger UI for testing
- Deployed on Render

---

## 🧠 What This Project Does

Amazon Bedrock Agents support memory and orchestration across multiple user interactions.

This API:
- Accepts user input via REST endpoints
- Maintains conversation context using agent memory / session IDs
- Forwards requests to a Bedrock Agent
- Returns intelligent, context-aware responses
- Acts as a backend service for chatbots, customer-support agents, or AI applications

---

## 📦 Tech Stack

- Python
- FastAPI
- Uvicorn
- Amazon Bedrock Agents
- Render (deployment)

---

## 📁 Project Structure

bedrock-agent-api/
│
├── main.py # FastAPI app with memory/session handling
├── requirements.txt # Python dependencies
├── README.md # Documentation


---

## ⚙️ Prerequisites

- Python 3.9+
- AWS account with Bedrock Agent access
- Configured Bedrock Agent with memory enabled
- Valid AWS credentials

---

## 🔐 Environment Variables

Set the following environment variables before running:

```bash
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=your_region

BEDROCK_AGENT_ID=your_agent_id
BEDROCK_AGENT_ALIAS_ID=your_agent_alias_id
🚀 Run Locally
Clone the repository:

git clone https://github.com/manjeet826510/bedrock-agent-api.git
cd bedrock-agent-api
Install dependencies:

pip install -r requirements.txt
Start the server:

uvicorn main:app --reload
Open in browser:

API: http://127.0.0.1:8000

Docs: http://127.0.0.1:8000/docs

📡 API Usage (With Memory)
The API supports session-based memory.

Example request:

{
  "session_id": "user_123",
  "input": "Hello, can you remember my name?"
}
Subsequent requests using the same session_id will retain context.

Example curl:

curl -X POST http://127.0.0.1:8000/ask \
-H "Content-Type: application/json" \
-d '{"session_id":"user_123","input":"What did I ask you earlier?"}'
☁️ Deployment
This API is deployed on Render.

🔗 Live Swagger Docs:
https://bedrock-agent-api.onrender.com/docs

🧩 Real-World Use Cases
Customer support AI agents

Conversational chatbots with memory

Enterprise AI assistants

API backend for Bedrock-powered apps

