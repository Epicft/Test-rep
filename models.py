from typing import Optional
from pydantic import BaseModel, ConfigDict


class STaskAdd(BaseModel):
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class STask(STaskAdd):
    id: int
    name: str
    description: Optional[str] = None
    is_completed: bool = False
    
    model_config = ConfigDict(from_attributes=True)
    

class STaskId(BaseModel):
    ok: bool = True
    task_id: int
    
    model_config = ConfigDict(from_attributes=True)