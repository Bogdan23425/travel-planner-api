from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Project
from app.models import ProjectPlace
from app.schemas.project import ProjectCreate
from app.schemas.project import ProjectUpdate
from app.schemas.project import ProjectResponse
from app.services.art_api import ArtApiUnavailable
from app.services.art_api import get_artwork

router = APIRouter(
    prefix='/projects',
    tags=['Projects'],
)

@router.post(
    "",
    response_model= ProjectResponse,
    status_code= 201,
)
def create_project(
    payload:ProjectCreate,
    db: Session = Depends(get_db),
):
    external_ids = [
        place.external_id
        for place in payload.places
    ]

    if len(external_ids) != len(set(external_ids)):
        raise HTTPException(
            status_code= 400,
            detail= "Duplicate places are not allowed",
        )

    validated_places = []

    for place_data in payload.places:
        try:
            artwork = get_artwork(place_data.external_id)
        except ArtApiUnavailable:
            raise HTTPException(
                status_code=503,
                detail="Art Institute API is unavailable",
            )

        if not artwork:
            raise HTTPException(
                status_code= 404,
                detail= f"Artwork {place_data.external_id} not found",
            )

        validated_places.append(
            {
                "external_id": place_data.external_id,
                "title": artwork.get("title", "Unknown Artwork"),
                "notes": place_data.notes,
            }
        )

    project = Project(
        name=payload.name,
        description=payload.description,
        start_date=payload.start_date,
    )

    try:
        db.add(project)
        db.flush()

        for place_data in validated_places:
            place = ProjectPlace(
                project_id=project.id,
                external_id=place_data["external_id"],
                title=place_data["title"],
                notes=place_data["notes"],
            )
            db.add(place)

        db.commit()
        db.refresh(project)
    except Exception:
        db.rollback()
        raise

    return project

@router.get(
    "",
    response_model=List[ProjectResponse],
)
def get_projects(
    db: Session = Depends(get_db),
):
    return db.query(Project).all()

@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code= 404,
            detail= "Project not found",
        )
    return project

@router.patch(
    "/{project_id}",
    response_model= ProjectResponse,
)
def update_project(
    project_id:int,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code= 404,
            detail= "Project not found",
        )
    data = payload.model_dump(
        exclude_unset= True,
    )

    for field, value in data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project
    
@router.delete(
    "/{project_id}",
    status_code= 204,
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code= 404,
            detail= "Project not found",
        )
    visited_places = (
        db.query(ProjectPlace)
        .filter(
            ProjectPlace.project_id == project_id,
            ProjectPlace.visited == True,
        )
        .count()
    )

    if visited_places:
        raise HTTPException(
            status_code= 400,
            detail="Cannot delete project with visited places",
        )
    db.delete(project)
    db.commit()
