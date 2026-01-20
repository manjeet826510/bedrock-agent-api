import os
import json
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
from dotenv import load_dotenv

# Load env vars
load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
AGENT_RUNTIME_ARN = os.getenv("BEDROCK_AGENT_RUNTIME_ARN")

if not all([AWS_REGION, AGENT_RUNTIME_ARN]):
    raise RuntimeError("Missing required environment variables")

app = FastAPI(
    title="Customer Care AI Agent (Bedrock Agent Core)",
    description="Public API wrapper for Amazon Bedrock Agent Core",
    version="1.0.0"
)

client = boto3.client(
    "bedrock-agentcore",
    region_name=AWS_REGION
)

# ---------- Request Model (Swagger sees ONLY this) ----------
class AgentRequest(BaseModel):
    prompt: str


# ---------- Helpers ----------
def generate_actor_id() -> str:
    # Later: replace with auth user id / API key owner
    return "public-user"


def generate_session_id() -> str:
    """
    Bedrock Agent Core requires runtimeSessionId >= 33 chars
    """
    return f"session-{uuid.uuid4().hex}"  # ~39 chars


# ---------- API ----------
@app.post("/chat")
def chat(req: AgentRequest):
    try:
        actor_id = generate_actor_id()
        session_id = generate_session_id()

        payload = json.dumps({
            "prompt": req.prompt,
            "actor_id": actor_id,
            "thread_id": session_id
        })

        response = client.invoke_agent_runtime(
            agentRuntimeArn=AGENT_RUNTIME_ARN,
            runtimeSessionId=session_id,
            payload=payload
        )

        response_body = response["response"].read()
        data = json.loads(response_body)

        # Extract clean values
        response1 = data.get("result", {})

        return {
            "result": response1
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
