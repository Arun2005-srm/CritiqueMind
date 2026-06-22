# server.py
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

# Import your compiled LangGraph workflow
from graph import app as langgraph_app

app = FastAPI(title="AgentOS Production Sandbox UI", version="1.0.0")

# 🛠️ FORCED ABSOLUTE RESOLUTION: Calculates the absolute path regardless of shell execution context
BASE_DIR = Path(__file__).resolve().parent
STATIC_FILE_PATH = (BASE_DIR / "static" / "index.html").resolve()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptPayload(BaseModel):
    prompt: str

@app.post("/api/generate")
async def generate_content(payload: PromptPayload):
    user_prompt = payload.prompt.strip()
    if not user_prompt:
        raise HTTPException(status_code=400, detail="Target prompt cannot be empty.")
    
    execution_payload = {
        "messages": [HumanMessage(content=user_prompt)],
        "is_approved": False,
        "loop_counter": 0,
        "rejection_reasons": [],
        "estimated_token_inflation": 0
    }
    
    try:
        final_state = langgraph_app.invoke(
            execution_payload, 
            {"configurable": {"thread_id": "web_production_run"}}
        )
        
        last_message_text = final_state["messages"][-1].content.strip()
        if last_message_text.startswith("APPROVED") or "APPROVED" in last_message_text[:20].upper():
            final_report_content = final_state["messages"][-2].content.strip()
        else:
            final_report_content = last_message_text

        return {
            "status": "success",
            "final_output": final_report_content,
            "loop_cycles": final_state.get("loop_counter", 0),
            "rejection_reasons": final_state.get("rejection_reasons", []),
            "token_metrics": final_state.get("estimated_token_inflation", 0)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route to serve frontend using the absolute string path securely
@app.get("/")
async def serve_index():
    # Double-check existence explicitly before sending to prevent unhandled ASGI app crashes
    if not STATIC_FILE_PATH.exists():
        raise HTTPException(
            status_code=500, 
            detail=f"Frontend index.html asset is missing on disk. Python searched path: {STATIC_FILE_PATH}"
        )
    # Convert Path object to an explicit string path for Windows stability
    return FileResponse(str(STATIC_FILE_PATH))