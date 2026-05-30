from typing import List
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Project
from app.models import ProjectPlace
from app.schemas.place import PlaceCreate
from app.schemas.place import PlaceUpdate
from app.schemas.place import PlaceResponse

router = APIRouter(
    prefix="/projects/{project_id}/places",
    tags=['Places'],
)

@router.post(
    "",
    response_model=PlaceResponse,
    status_code= 201,
)
def create_place(
    project_id: int,
    payload: PlaceCreate,
    db: Session = Depends(get_db),
):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code= 404,
            detail= "Project not found",
        )
    place = ProjectPlace(
        project_id= project.id,
        external_id= payload.external_id,
        title= payload.title,
        notes= payload.notes,
    )
    db.add(place)
    db.commit()
    db.refresh(place)

    return place

@router.get(
        "",
        response_model=List[PlaceResponse],
)
def get_places(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code= 404,
            detail= "Project not found",
        )
    
    return(
        db.query(ProjectPlace)
        .filter(ProjectPlace.project_id == project_id)
        .all()
    )

@router.get(
    "/{place_id}",
    response_model=PlaceResponse,
)
def get_place(
    project_id: int,
    place_id: int,
    db: Session = Depends(get_db),
):
    place = (
        db.query(ProjectPlace)
        .filter(
            ProjectPlace.project_id == project_id,
            ProjectPlace.id == place_id,
        )
        .first()
    )
    if not place:
        raise HTTPException(
            status_code= 404,
            detail="Place not found",
        )
    return place

@router.patch(
    "/{place_id}",
    response_model=PlaceResponse,
)
def update_place(
        project_id:int,
        place_id: int,
        payload: PlaceUpdate,
        db: Session = Depends(get_db),
):
    place = (
        db.query(ProjectPlace)
        .filter(
            ProjectPlace.project_id == project_id,
            ProjectPlace.id == place_id,
        )
        .first()
    )
    if not place:
        raise HTTPException(
            status_code= 404,
            detail="Place not found",
        )
    data = payload.model_dump(
        exclude_unset=True,
    )

    for field, value in data.items():
        setattr(place, field, value)

    db.commit()
    db.refresh(place)

    return place