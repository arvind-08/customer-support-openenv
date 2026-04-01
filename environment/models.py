from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class Observation(BaseModel):
    """
    What the agent sees after each step
    """

    ticket_id: str
    customer_message: str
    conversation_history: List[str]
    available_actions: List[str]
    status: str
    metadata: Optional[Dict[str, Any]] = None


class Action(BaseModel):
    """
    What the agent sends to environment
    """

    action_type: str
    content: Optional[str] = None


class Reward(BaseModel):
    """
    Reward returned after each step
    """

    score: float
    message: Optional[str] = None


class State(BaseModel):
    """
    Internal environment state
    """

    ticket_id: str
    customer_message: str
    conversation_history: List[str]
    classification: Optional[str] = None
    resolved: bool = False
    step_count: int = 0