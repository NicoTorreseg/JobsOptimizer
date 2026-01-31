from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

class JobOfferBase(BaseModel):
    title: str
    company_name: str
    location: Optional[str] = None
    url: HttpUrl
    description_raw: Optional[str] = None
    seniority: Optional[str] = None
    salary_range: Optional[str] = None
    remote: bool = False
    posted_at: Optional[datetime] = None
    tech_stack: List[str] = []

class JobOfferCreate(JobOfferBase):
    pass

class JobOffer(JobOfferBase):
    id: int
    company_id: int
    created_at: datetime

    class Config:
        from_attributes = True
