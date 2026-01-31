from abc import ABC, abstractmethod
from typing import List
import httpx
from app.schemas.job import JobOfferCreate

class BaseScraper(ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    async def fetch_page(self, url: str) -> str:
        """Downloads the HTML content of the page."""
        async with httpx.AsyncClient(headers=self.headers, follow_redirects=True) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                return response.text
            except httpx.HTTPStatusError as e:
                print(f"Error fetching {url}: {e}")
                return ""
            except Exception as e:
                print(f"Connection error {url}: {e}")
                return ""

    @abstractmethod
    def parse(self, html_content: str) -> List[JobOfferCreate]:
        """Parses the HTML and extracts job offers."""
        pass

    @abstractmethod
    async def scrape(self) -> List[JobOfferCreate]:
        """Main method to execute the scraping logic."""
        pass
