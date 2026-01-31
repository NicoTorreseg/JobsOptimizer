from sqlalchemy.orm import Session
from app.models.job import JobOffer, Company
from app.schemas.job import JobOfferCreate
import hashlib
from datetime import datetime

class IngestionService:
    def __init__(self, db: Session):
        self.db = db

    def _generate_content_hash(self, offer: JobOfferCreate) -> str:
        """Create a hash based on title and company to detect duplicates."""
        # Simple strategy: Hash(Title + Company + Link)
        # Using link is safer to distinguish similar roles in same company if specific
        unique_string = f"{offer.title}{offer.company_name}{offer.url}".lower().encode('utf-8')
        return hashlib.sha256(unique_string).hexdigest()

    def _normalize_title(self, title: str) -> str:
        """Basic normalization logic."""
        title_lower = title.lower()
        if "python" in title_lower and "developer" in title_lower:
            return "Python Developer"
        if "backend" in title_lower:
            return "Backend Developer"
        if "data scientist" in title_lower:
            return "Data Scientist"
        return title # Fallback

    def _get_or_create_company(self, name: str) -> Company:
        company = self.db.query(Company).filter(Company.name == name).first()
        if not company:
            # Create slug (very basic implementation)
            slug = name.lower().replace(" ", "-").replace(".", "").replace(",", "")
            company = Company(name=name, slug=slug)
            self.db.add(company)
            self.db.commit()
            self.db.refresh(company)
        return company

    def process_job_offer(self, offer_data: JobOfferCreate) -> JobOffer | None:
        """
        Main pipeline:
        1. Hash Check (Deduplication)
        2. Normalization
        3. Persistence
        """
        content_hash = self._generate_content_hash(offer_data)
        
        # Check if exists
        existing_job = self.db.query(JobOffer).filter(JobOffer.content_hash == content_hash).first()
        if existing_job:
            print(f"Skipping duplicate: {offer_data.title} at {offer_data.company_name}")
            return None

        # Normalize
        normalized_title = self._normalize_title(offer_data.title)
        
        # Get Company
        company = self._get_or_create_company(offer_data.company_name)
        
        # Create Job
        new_job = JobOffer(
            company_id=company.id,
            title=offer_data.title,
            normalized_title=normalized_title,
            description_raw=offer_data.description_raw or "",
            seniority=offer_data.seniority or "Not Specified",
            tech_stack=offer_data.tech_stack,
            content_hash=content_hash,
            url=str(offer_data.url),
            location=offer_data.location,
            created_at=datetime.utcnow()
        )
        
        self.db.add(new_job)
        self.db.commit()
        self.db.refresh(new_job)
        print(f"Ingested: {new_job.title} ({new_job.id})")
        return new_job
