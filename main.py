import os
import json
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
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
    prompt: str = Field(
        ...,
        example="Type your prompt here"
    )
    session_id: str | None = Field(
        default=None,
        example="user-session-00000000000000000001",
        description=(
            "Enter a session id with at least 34 characters. "
            "Use the SAME session_id for subsequent requests to maintain conversation context."
        )
    )




# ---------- Helpers ----------
def generate_actor_id() -> str:
    # Later: replace with auth user id / API key owner
    return "public-user"

def get_session_id(req: AgentRequest) -> str:
    if req.session_id and len(req.session_id) >= 33:
        return req.session_id
    
    # fallback default session
    return "public-session-000000000000000000000"



# ---------- API ----------
@app.post(
    "/chat",
    summary="Chat with the Customer Care AI Agent",
    description="Send a prompt to the AI agent. Reuse the same session_id across requests to maintain conversation context."
)
def chat(req: AgentRequest):
    try:
        actor_id = "public-user"
        session_id = get_session_id(req)

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

        return {"result": data["result"], "session_id": session_id}


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
