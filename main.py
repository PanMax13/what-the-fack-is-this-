from fastapi import FastAPI, Depends
from sqlalchemy.future import select
from db_connect import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from models import User, Project, UserProject
from sqlalchemy import text

app = FastAPI()

@app.get('/')
async def main():
    return {"to users": "/users"}



@app.get('/users/{id}')
async def users(id: int, session: AsyncSession = Depends(get_db)):
    user = await session.execute(select(User).filter(User.id == id))
    user = user.scalars()
    user = user.one_or_none()
    user_projects = await session.execute(text(f'SELECT * FROM user_projects WHERE user_projects.user_id = {id};'))

    projects = []
    for x in user_projects:
        project_name = await session.execute(text(f'SELECT projects.name FROM projects WHERE projects.id = {id}'))
        projects.append(project_name.scalar())

    if user is None:
        return {"error": "User is not found"}

    return {
        "User": user.name,
        "Projects": projects
    }

@app.get('/projects/{id}')
async def projects(id: int, session: AsyncSession = Depends(get_db)):
    project = await session.execute(select(Project).filter(Project.id == id))
    project = project.scalars()
    project = project.one_or_none()

    if project is None:
        return {"Error" : "Project is not found"}


    project_users = await session.execute(text(f"SELECT user_projects.user_id FROM user_projects WHERE user_projects.project_id = {id};"))
    project_users = project_users.scalars()

    users = []

    for x in project_users:
        project_user = await session.execute(text(f'SELECT users.name FROM users WHERE users.id = {x};'))
        users.append(project_user.scalar())


    return {
        "Project" : project.name,
        "Users": users
    }