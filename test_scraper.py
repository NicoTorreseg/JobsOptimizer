import asyncio
import sys
import os

# Add the backend directory to sys.path so we can import from app
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

# from app.scrapers.python_org import PythonOrgScraper
from app.scrapers.computrabajo import CompuTrabajoScraper

async def main():
    print("Iniciando scraper de prueba (CompuTrabajo)...")
    # scraper = PythonOrgScraper()
    scraper = CompuTrabajoScraper()
    jobs = await scraper.scrape()
    
    print(f"Se encontraron {len(jobs)} ofertas:")
    print("-" * 50)
    for job in jobs[:5]: # Mostrar solo las primeras 5
        print(f"Título: {job.title}")
        print(f"Empresa: {job.company_name}")
        print(f"Ubicación: {job.location}")
        print(f"URL: {job.url}")
        print(f"Stack: {job.tech_stack}")
        print("-" * 50)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error ejecutando el scraper: {e}")
