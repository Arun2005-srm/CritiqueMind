# state.py
from typing import Annotated
from typing_extensions import TypedDict
from operator import add
from langchain_core.messages import AnyMessage

class AdvancedPipelineState(TypedDict):
    messages: Annotated[list[AnyMessage], add]   # Appends history automatically
    is_approved: bool                             # Overwrites state on approval check
    loop_counter: int                             # Overwrites state to track depth
    rejection_reasons: Annotated[list[str], add]  # Appends historical failure vectors
    estimated_token_inflation: int                # Overwrites context payload size metrics