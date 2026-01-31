import asyncio
import sys
import os
from sqlalchemy.orm import Session

# Add the backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from app.scrapers.python_org import PythonOrgScraper
from app.core.database import SessionLocal
from app.services.ingestion import IngestionService

async def run_pipeline():
    print("--- Starting Pipeline ---")
    
    # 1. Scrape
    print("[1/2] Scraping Python.org...")
    scraper = PythonOrgScraper()
    scraped_jobs = await scraper.scrape()
    print(f"Found {len(scraped_jobs)} raw jobs.")

    # 2. Ingest
    print("[2/2] Ingesting to Database...")
    db = SessionLocal()
    ingestion = IngestionService(db)
    
    count_new = 0
    for job_data in scraped_jobs:
        try:
            job = ingestion.process_job_offer(job_data)
            if job:
                count_new += 1
        except Exception as e:
            print(f"Error processing job {job_data.title}: {e}")
            db.rollback()
    
    db.close()
    print(f"--- Pipeline Finished. ingested {count_new} new jobs. ---")

if __name__ == "__main__":
    asyncio.run(run_pipeline())
