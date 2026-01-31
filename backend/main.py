from fastapi import FastAPI
from app.routers import jobs
from app.core.database import Base, engine

# Create tables if not exists (redundant if using alembic, but good for dev)
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="JobsOptimizer API", version="0.1.0")

app.include_router(jobs.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to JobsOptimizer API"}
