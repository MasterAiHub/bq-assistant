from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TranscriptSegment(BaseModel):
    speaker: str
    text: str
    timestamp: datetime

class Meeting(BaseModel):
    id: Optional[str] = None
    user_id: str
    title: str
    start_time: datetime
    end_time: Optional[datetime] = None
    transcript: List[TranscriptSegment] = []
    summary: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
