from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict


class PlaceCreate(BaseModel):
    external_id:int
    notes:str | None = None


class PlaceUpdate(BaseModel):
    notes:str | None = None
    visited:bool | None = None

class PlaceResponse(BaseModel):
    id:int
    project_id: int
    external_id: int
    title:str
    notes:str | None
    visited: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )