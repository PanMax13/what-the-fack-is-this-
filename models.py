from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase, MappedColumn
from dotenv import load_dotenv


# TODO: создать 2 сущности: пользователь и проект. У проекта может быть привязано несколько пользователей,
#  у пользователя может быть больше, чем 1 проект

load_dotenv()



class Base(DeclarativeBase):
    pass

class UserProject(Base):
    __tablename__ = 'user_projects'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True)

    project_id: Mapped[int] = mapped_column(
        ForeignKey('projects.id', ondelete='CASCADE'),
        primary_key=True)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)

    projects: Mapped[list["Project"]] = relationship(
        'Project',
        secondary='user_projects',
        back_populates='users')

class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)

    users: Mapped[list["User"]] = relationship(
        'User',
        secondary='user_projects',
        back_populates='projects'
    )

