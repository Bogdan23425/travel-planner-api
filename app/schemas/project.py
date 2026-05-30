from datetime import date
from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import model_validator

from app.schemas.place import PlaceCreate
from app.schemas.place import PlaceResponse

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    start_date:date | None = None
    places: list[PlaceCreate] = Field(
        ...,
        min_length=1,
        max_length=10,
    )

class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    start_date:date | None = None

    @model_validator(mode="after")
    def validate_not_empty(self):
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided")
        return self

class ProjectResponse(BaseModel):
    id:int
    name:str
    description:str | None
    start_date: date | None
    is_completed:bool
    created_at:datetime
    places:list[PlaceResponse] = Field(default_factory=list)

    model_config = ConfigDict(
        from_attributes=True,
    )
