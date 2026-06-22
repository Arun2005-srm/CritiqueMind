# main.py
import os
import sys
from langchain_core.messages import HumanMessage
from graph import app

if __name__ == "__main__":
    print("====================================================", flush=True)
    print("🤖 AgentOS Production Sandbox Environment Initialized", flush=True)
    print("====================================================", flush=True)
    
    sys.stdout.flush()
    user_prompt = input("\n🎯 Target Task/Topic to Execute: ")
    
    if not user_prompt.strip():
        print("❌ Error: Input target payload cannot be empty.", flush=True)
        exit(1)
        
    execution_payload = {
        "messages": [HumanMessage(content=user_prompt)],
        "is_approved": False,
        "loop_counter": 0,
        "rejection_reasons": [],
        "estimated_token_inflation": 0
    }

    print("\n🚀 Commencing Agent Collaboration Framework...", flush=True)
    final_state = app.invoke(execution_payload, {"configurable": {"thread_id": "production_run_9"}})
    
    print("\n====================================================", flush=True)
    print("📊 AGENTOS CONTROL PLANE OBSERVABILITY LOG", flush=True)
    print("====================================================", flush=True)
    print(f"Loop Iteration Sump: {final_state['loop_counter']} cycles", flush=True)
    print(f"Memory Footprint Mass: {final_state['estimated_token_inflation']} memory trace metrics", flush=True)
    
    print("Audit Trace Vectors:", flush=True)
    for idx, fault in enumerate(final_state["rejection_reasons"], 1):
        print(f"  [Fault Pattern {idx}]: {fault}", flush=True)
        
    # Smart Text Asset Extraction Logic
    last_message_text = final_state["messages"][-1].content.strip()
    if last_message_text.startswith("APPROVED") or "APPROVED" in last_message_text[:20].upper():
        final_report_content = final_state["messages"][-2].content.strip()
    else:
        final_report_content = last_message_text
        
    print("\n====================================================", flush=True)
    print("📝 FINAL COLLABORATIVE GENERATED CONTENT ASSET", flush=True)
    print("====================================================", flush=True)
    print(final_report_content, flush=True)
    print("====================================================\n", flush=True)

    # Save to Markdown Document
    safe_filename = "final_output_report.md"
    try:
        with open(safe_filename, "w", encoding="utf-8") as file:
            file.write(f"# Compiled Multi-Agent Production Report\n\n")
            file.write(f"**Original Prompt:** {user_prompt}\n")
            file.write(f"**Total Loop Cycles:** {final_state['loop_counter']}\n")
            file.write(f"---\n\n")
            file.write(final_report_content)
            
        print(f"💾 SYSTEM SUCCESS: Final asset cleanly compiled and saved to disk!")
        print(f"📂 File Location: {os.path.abspath(safe_filename)}\n", flush=True)
    except Exception as e:
        print(f"❌ Failed to save file down to disk: {e}", flush=True)