import uvicorn
from fastapi import FastAPI
from app.tasks import routes as task_routes
from app.auth import routes as auth_routes
from app.core import database, models

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(task_routes.router)

if __name__ == "__main__":
    uvicorn.run('app.main:app', reload=True, host='0.0.0.0')