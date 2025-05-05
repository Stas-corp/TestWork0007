import uvicorn
from fastapi import FastAPI
from app.tasks import routes
from app.auth import routes
from app.core import database, models

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(routes.router)
app.include_router(routes.router)

if __name__ == "__main__":
    uvicorn.run('app.main:app', reload=True)