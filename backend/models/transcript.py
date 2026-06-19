from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Transcript(BaseModel):
    id: Optional[str] = None
    meeting_id: str
    user_id: str
    content: str
    created_at: datetime = datetime.utcnow()
