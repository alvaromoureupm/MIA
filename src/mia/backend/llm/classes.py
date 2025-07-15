from pydantic import BaseModel
from langchain_core.documents import Document
from typing_extensions import List, TypedDict
from typing import Optional

class MiaState(TypedDict):
    """
    State model
    """
    question: str
    answer: str
    context = List[Document]
    summary = Optional[str]