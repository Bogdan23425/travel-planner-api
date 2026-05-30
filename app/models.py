from datetime import date
from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database import Base

class Project(Base):
    __tablename__= 'projects'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key = True,
        index = True,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable = False,
    )
    
    description: Mapped [str | None] = mapped_column(
        Text,
        nullable = True,
    )
    start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable = True,
    )
    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        default = False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default = datetime.utcnow,
    )

    places = relationship(
        'ProjectPlace',
        back_populates = 'project',
        cascade = "all, delete-orphan",
    )

class ProjectPlace(Base):
    __tablename__ = 'project_places'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key = True,
        index = True,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey('projects.id'),
    )
    external_id: Mapped[int] = mapped_column(
        Integer,
        nullable = False,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable = False,
    )
    notes: Mapped [str | None] = mapped_column(
        Text,
        nullable = True,
    )

    visited: Mapped[bool] = mapped_column(
        Boolean,
        default = False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default = datetime.utcnow,
    )

    project = relationship(
        'Project',
        back_populates = 'places',
    )