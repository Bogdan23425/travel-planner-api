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
    payload: ProjectCreate,
    db: Session = Depends(get_db),
):
    project = Project(
        name = payload.name,
        description = payload.description,
        start_date = payload.start_date,
    )
    db.add(project)
    db.commit()
    db.refresh(project)

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