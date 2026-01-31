from typing import List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper
from app.schemas.job import JobOfferCreate
from datetime import datetime

class PythonOrgScraper(BaseScraper):
    def __init__(self):
        super().__init__(base_url="https://www.python.org/jobs/")

    def parse(self, html_content: str) -> List[JobOfferCreate]:
        soup = BeautifulSoup(html_content, "html.parser")
        jobs = []
        
        # Select the list of jobs
        job_list = soup.find("ol", class_="list-recent-jobs")
        if not job_list:
            return []

        for li in job_list.find_all("li"):
            title_tag = li.find("span", class_="listing-company-name").find("a")
            
            # Extract company name safely (text nodes only, excluding children like 'listing-location')
            company_span = li.find("span", class_="listing-company-name")
            company_name = "Unknown"
            if company_span:
                # Get text directly inside the span, excluding children
                text_nodes = [text for text in company_span.find_all(string=True, recursive=False) if text.strip()]
                if text_nodes:
                    company_name = text_nodes[0].strip()
                    # Remove "posted on" or similar artifacts if present, though python.org usually has clean text here
                    if "Company" in company_span.get_text() and not text_nodes: 
                         # Fallback if structure is complex
                         pass

            # Category/Tags often implies tech stack or type
            category_tag = li.find("span", class_="listing-job-type")
            job_type = category_tag.get_text(strip=True) if category_tag else "Unknown"

            location_tag = li.find("span", class_="listing-location")
            location = location_tag.get_text(strip=True) if location_tag else None
            
            if title_tag:
                title = title_tag.get_text(strip=True)
                url = "https://www.python.org" + title_tag["href"]
                
                # Simple normalization (very basic for prototype)
                tech_stack = ["Python"] 
                
                job = JobOfferCreate(
                    title=title,
                    company_name=company_name.strip().rstrip(","), # Clean trailing commas
                    location=location,
                    url=url,
                    description_raw=f"Job Type: {job_type}", # Currently we don't visit the detail page in this prototype
                    posted_at=datetime.utcnow(), # Placeholder as valid date parsing needs format check
                    tech_stack=tech_stack,
                    remote="Remote" in location if location else False
                )
                jobs.append(job)
        
        return jobs

    async def scrape(self) -> List[JobOfferCreate]:
        html = await self.fetch_page(self.base_url)
        if html:
            return self.parse(html)
        return []
