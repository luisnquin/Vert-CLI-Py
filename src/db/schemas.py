from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    datetime: Optional[datetime] = None
