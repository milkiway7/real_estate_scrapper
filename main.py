import asyncio
from Scrappers.oto_dom_scrapper import OtoDomScraper
from Helpers.logger import get_logger

async def main():
    try:
        oto_dom_scraper = OtoDomScraper("Kraków")
        await oto_dom_scraper.run_oto_dom_scraper()
    except Exception as e:
        get_logger.error(f"An error occurred in the main function: {e}")
if __name__ == "__main__":
    asyncio.run(main())