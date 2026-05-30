from datetime import date
from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict

class ProjectCreate(BaseModel):
    name:str
    description:str | None = None
    start_date:date | None = None

class ProjectUpdate(BaseModel):
    name:str | None = None
    description:str | None = None
    start_date:date | None = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description:str | None
    start_date:date | None
    is_completed: bool
    created_at:datetime

    model_config = ConfigDict(
        from_attributes=True,
    )