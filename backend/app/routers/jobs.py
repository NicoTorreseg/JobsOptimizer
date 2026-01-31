from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.job import JobOffer
from app.schemas.job import JobOffer as JobOfferSchema

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)

@router.get("/", response_model=List[JobOfferSchema])
def read_jobs(
    skip: int = 0, 
    limit: int = 20, 
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(JobOffer)
    
    if search:
        # Simple case-insensitive search on normalized title
        search_fmt = f"%{search}%"
        query = query.filter(JobOffer.normalized_title.ilike(search_fmt))
        
    jobs = query.offset(skip).limit(limit).all()
    return jobs
