from pydantic import BaseModel, ConfigDict
from typing import Optional

class IOCTypeResponse(BaseModel):
    id: int
    name: str
    category: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)