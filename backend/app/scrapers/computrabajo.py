from typing import List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper
from app.schemas.job import JobOfferCreate
from datetime import datetime
import traceback
import re

class CompuTrabajoScraper(BaseScraper):
    def __init__(self):
        # Using a generic search URL for Python jobs in Argentina
        super().__init__(base_url="https://ar.computrabajo.com/trabajo-de-python")
        # Overwrite headers to look like a real browser to avoid 403
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            "Referer": "https://ar.computrabajo.com/",
            "Connection": "keep-alive"
        }

    def parse(self, html_content: str) -> List[JobOfferCreate]:
        soup = BeautifulSoup(html_content, "html.parser")
        jobs = []

        # CompuTrabajo usually lists offers in <article class="box_offer">
        # Note: Classes often change. We use the one requested by the user but should be robust.
        articles = soup.find_all("article", class_="box_offer")
        
        if not articles:
            # Fallback or logging if structure changed
            print("Warning: No articles found with class 'box_offer'. Layout might have changed.")
            return []

        for article in articles:
            try:
                # Title is usually in an h1 or h2 with class 'title_offer' or inside a link
                title_tag = article.find("h1") or article.find("h2") or article.find("p", class_="title_offer")
                title = title_tag.get_text(strip=True) if title_tag else "Sin título"
                
                # CLEAN TITLE
                # Remove "Postulado", "Vista", "Nuevo" logic
                for bad_word in ["Postulado", "Vista", "Nuevo"]:
                    title = title.replace(bad_word, "")
                title = title.strip()
                
                # Link
                link_tag = article.find("a", href=True)
                # Ensure absolute URL
                url = link_tag["href"] if link_tag else ""
                if url and not url.startswith("http"):
                    url = f"https://ar.computrabajo.com{url}"

                # Company - often in a <p> or link
                # Sometimes it's hidden or just text
                company_tag = article.find("div", class_="fs16") or article.find("p", class_="fs16")
                company_name = company_tag.get_text(strip=True) if company_tag else "Confidencial"
                
                # CLEAN COMPANY NAME
                # Remove leading rating like "4,2"
                company_name = re.sub(r'^\d+,\d+\s*', '', company_name).strip()
                
                # Location - often in a span or p
                location_tag = article.find("p", class_="fs13") 
                location = "Argentina"
                if location_tag:
                     # Often formatting is "Company - Location"
                     # Or separate tags. Let's try to extract basic text.
                     text_nodes = [t for t in location_tag.find_all(string=True) if t.strip()]
                     if len(text_nodes) > 1:
                         location = text_nodes[-1].strip() # Heuristic
                
                # Description logic (truncated in list view)
                description_tag = article.find("p", class_="details")
                description = description_tag.get_text(strip=True) if description_tag else ""

                # Tech stack inference (Basic)
                tech_stack = []
                lower_title = title.lower()
                if "python" in lower_title: tech_stack.append("Python")
                if "django" in lower_title: tech_stack.append("Django")
                if "flask" in lower_title: tech_stack.append("Flask")
                if "data" in lower_title: tech_stack.append("Data")

                if title != "Sin título" and url:
                    job = JobOfferCreate(
                        title=title,
                        company_name=company_name,
                        location=location,
                        url=url,
                        description_raw=description,
                        seniority="Not Specified", # Hard to get from list view reliably without parsing detail
                        posted_at=datetime.utcnow(),
                        tech_stack=tech_stack,
                        remote="remoto" in location.lower() or "remoto" in title.lower()
                    )
                    jobs.append(job)

            except Exception as e:
                print(f"Error parsing article: {e}")
                # traceback.print_exc()
                continue
                
        return jobs

    async def scrape(self) -> List[JobOfferCreate]:
        # Using the parent method but with our specific headers
        html = await self.fetch_page(self.base_url)
        if html:
            return self.parse(html)
        return []
