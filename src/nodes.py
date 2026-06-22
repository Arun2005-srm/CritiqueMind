# nodes.py
import os
import yaml
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from state import AdvancedPipelineState

# ==========================================
# 🔌 AGENTOS CONFIGURATION PLANE INGESTION
# ==========================================
CONFIG_PATH = "config.yaml"

if not os.path.exists(CONFIG_PATH):
    print(f"❌ CRITICAL ERROR: System Manifest missing at '{CONFIG_PATH}'. Please build your config file.")
    exit(1)

with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    system_config = yaml.safe_load(file)

# Securely bind the key directly into the application space environment matrix
os.environ["GROQ_API_KEY"] = system_config["credentials"]["groq_api_key"]

# Initialize compute models using configurations from our YAML manifest
model = ChatGroq(
    model=system_config["orchestration"]["model_name"], 
    temperature=system_config["orchestration"]["temperature"]
)

# ==========================================
# 🧠 AGENTOS KERNEL: MEMORY OPTIMIZATION LAYER
# ==========================================
def agentos_compress_context(history: list) -> list:
    """Saves token overhead by dynamically sliding the context window."""
    if len(history) <= 3:
        return history
    print(f"⚙️  [AgentOS Kernel]: Optimizing memory plane. Pruning context overhead...")
    return [history[0]] + history[-2:]

# ==========================================
# 2. COLLABORATIVE MULTI-AGENT NODES
# ==========================================

def writer_node(state: AdvancedPipelineState):
    """The Writer: Generates assets and refines text based on settings maps."""
    history = state["messages"]
    next_loop_value = state["loop_counter"] + 1
    
    system_prompt = SystemMessage(content=(
        "You are an expert technical copywriter. Your goal is to draft a clean, "
        "persuasive response to the prompt. Look at the recent history and address "
        "the critic's adjustments precisely while maintaining structural clarity. "
        "Only output your draft. Do not include chatty introductions or metadata."
    ))
    
    optimized_history = agentos_compress_context(history)
    response = model.invoke([system_prompt] + optimized_history)
    print(f"✍️  [WRITER] (Iteration {next_loop_value}): Compiling updated draft asset...", flush=True)
    
    return {
        "messages": [response],
        "loop_counter": next_loop_value
    }

def critic_node(state: AdvancedPipelineState):
    """The Critic: Audits content drafts against rigid semantic quality bounds."""
    history = state["messages"]
    
    system_prompt = SystemMessage(content=(
        "You are a ruthless Quality Assurance Editor. Review the last draft from the Writer.\n"
        "CRITERIA:\n"
        "1. Must be deeply educational, accurate, and professional.\n"
        "2. Must NOT contain cliches, fluff, or hand-waving conclusions.\n\n"
        "VERDICT RULES:\n"
        "If it meets all criteria perfectly, start your response with the exact word: APPROVED.\n"
        "If it fails, start your response with: REJECTED - [State core reason here]. Then provide detailed feedback."
    ))
    
    optimized_history = agentos_compress_context(history)
    response = model.invoke([system_prompt] + optimized_history)
    
    # FIX 1: Strip leading/trailing whitespaces/newlines to capture the true verdict line
    verdict_text = response.content.strip()  
    is_approved = "APPROVED" in verdict_text[:20].upper()
    
    reason = "No issues found."
    if not is_approved:
        reason = verdict_text.split("\n")[0]
        print(f"🧐 [CRITIC]: Draft Rejected. Vector: {reason}", flush=True)
    else:
        print("🧐 [CRITIC]: Quality requirements satisfied! Marking state as Approved.", flush=True)

    context_footprint = len(str(history))
    
    return {
        "messages": [response],
        "is_approved": is_approved,
        "rejection_reasons": [reason] if not is_approved else [],
        "estimated_token_inflation": context_footprint
    }

def synthesizer_node(state: AdvancedPipelineState):
    """The Synthesizer: Resolves agent deadlocks to produce a compromise asset."""
    history = state["messages"]
    
    print("\n🚨 [CONTROL PLANE ALERT] Deadlock loop detected. Circuit breaker triggered.", flush=True)
    print("🧠 [SYNTHESIZER]: Intervening to arbitrate state conflict and finalize production...", flush=True)
    
    # FIX 2: Compile message objects into a flat text transcript to bypass API role-alternation bugs
    transcript_segments = []
    for idx, msg in enumerate(history):
        if idx == 0:
            role = "ORIGINAL USER PROMPT"
        else:
            role = "WRITER DRAFT" if idx % 2 != 0 else "CRITIC FEEDBACK"
        transcript_segments.append(f"=== {role} ===\n{msg.content}\n")
    
    full_transcript = "\n".join(transcript_segments)
    
    system_prompt = SystemMessage(content=(
        "You are the Chief Executive Editor. The Writer and Critic are trapped in an infinite "
        "argument loop and cannot agree. Review the provided message history transcript, extract the strongest points "
        "from the writer's latest version, correct them using the critic's valid objections, "
        "and produce the final polished output document. Do not include any chatty introductions or metadata; output ONLY the final text asset."
    ))
    
    transcript_payload = HumanMessage(content=f"Here is the compilation of the deadlocked session history:\n\n{full_transcript}")
    
    response = model.invoke([system_prompt, transcript_payload])
    
    return {
        "messages": [response],
        "is_approved": True
    }

def route_governor(state: AdvancedPipelineState):
    """Kernel Governance Router: Evaluates bounds using dynamic configuration threshold."""
    if state["is_approved"]:
        return "healthy_exit"
        
    max_allowed_depth = system_config["orchestration"]["max_loop_threshold"]
    if state["loop_counter"] >= max_allowed_depth:
        return "trigger_circuit_breaker"
        
    return "continue_iteration"