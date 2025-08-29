import httpx
from Helpers.logger import get_logger
import os
class ScrappedDataTableClient:
    def __init__(self):
        self.logger = get_logger()
        self.url_clear_table = os.getenv("DATA_ANALYSIS_URL") + "/clear_scrapped_data"
        self.url_set_sold_out = os.getenv("DATA_ANALYSIS_URL") + "/mark_soldout_for_nulls_scrapped_archive"
        self.timeout = httpx.Timeout(15.0)

    async def clear_scrapped_data(self):
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                self.logger.info(f"Sending request to delete scrapped data at {self.url_clear_table}")
                response = await client.delete(self.url_clear_table)
                response.raise_for_status()
                self.logger.info(f"Successfully copied and deleted scrapped data. Status code: {response.status_code}")
        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}") 

    async def mark_sold_out_for_nulls(self):
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                self.logger.info(f"Sending request to mark sold out for nulls at {self.url_set_sold_out}")
                response = await client.post(self.url_set_sold_out)
                response.raise_for_status()
                self.logger.info(f"Successfully marked sold out for nulls. Status code: {response.status_code}")
        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")