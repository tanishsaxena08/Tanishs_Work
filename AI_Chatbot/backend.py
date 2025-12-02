'''
Phase 2
Step 1: Setup Pydantic model (schema validation)
'''

# CODE STARTS HERE
from pydantic import BaseModel
from typing import List
from fastapi import FastAPI

from ai_agent import get_response_from_ai_agent

# Step 1: Define request schema
class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_provider: str
    messages: List[str]
    allow_search: bool

# Step 2: Setup FastAPI from frontenf request
ALLOWED_MODEL_NAMES = [
    "llama3-70b-8192",
    "mixtral-8x7b-32768",
    "llama-3.3-70b-versatile",
    "gpt-4o-mini"
]

app = FastAPI(title="LangGraph AI Chatbot Agent")

@app.post("/chat")
def chat_endpoint(request_state: RequestState):
    """
    Endpoint to handle chat requests.
    Interacts with the chatbot using LangGraph and optional search tools.
    Dynamically selects the model specified in the request.
    """
    if request_state.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Model not allowed, kindly select a valid AI model"}

    llm_id = request_state.model_name
    query = request_state.messages[-1]
    allow_search = request_state.allow_search
    system_prompt = request_state.system_provider
    provider = request_state.model_provider

    # Create AI Agent and get response
    response = get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider)
    return {"response": response}

# Step 3: Run app and explore Swagger UI Docs
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999)