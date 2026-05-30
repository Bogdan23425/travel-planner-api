from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import model_validator


class PlaceCreate(BaseModel):
    external_id: int = Field(..., gt=0)
    notes: str | None = Field(default=None, max_length=2000)


class PlaceUpdate(BaseModel):
    notes: str | None = Field(default=None, max_length=2000)
    visited:bool | None = None

    @model_validator(mode="after")
    def validate_not_empty(self):
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided")
        return self

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
