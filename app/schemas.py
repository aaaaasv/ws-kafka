import datetime

from pydantic import BaseModel


class Message(BaseModel):
    topic: str
    partition: int
    offset: int
    timestamp: datetime.datetime
    value: str
    timestamp_type: int
