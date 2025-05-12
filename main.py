import asyncio
from Scrapers.oto_dom_scrapper import OtoDomScraper

async def main():
    oto_dom_scraper = OtoDomScraper("Kraków")
    await oto_dom_scraper.run_oto_dom_scraper()

if __name__ == "__main__":
    asyncio.run(main())