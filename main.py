from dotenv import load_dotenv
load_dotenv()
import asyncio
import sys
from Scrappers.oto_dom_scrapper import OtoDomScraper
from Helpers.logger import get_logger
from DataClient.ScrappedDataTableClient import ScrappedDataTableClient

async def run_scrapper():
    try:
        # Save backup of scrapped data and scrapped data archive to the disc

        # Before scrapping, send api request to data analytics to copy data from ScrappingDataTable to ScrappedDataArchiveTable 
        # then delete data from ScrappingDataTable
        clear_scrapped_data_client = ScrappedDataTableClient()
        await clear_scrapped_data_client.clear_scrapped_data()
        # Run the scrapper
        oto_dom_scraper = OtoDomScraper("Kraków")
        await oto_dom_scraper.run_oto_dom_scraper()
        # Check differences between the data in ScrappingDataTable and ScrappedDataArchiveTable and fill SoldOutColumn in ScrappingDataTable
        # await clear_scrapped_data_client.mark_sold_out_for_nulls()
    except Exception as e:
        get_logger().error(f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    asyncio.run(run_scrapper())
    