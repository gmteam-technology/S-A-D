from datetime import datetime
from pydantic import BaseModel


class TimestampedSchema(BaseModel):
    created_at: datetime

    class Config:
        from_attributes = True
