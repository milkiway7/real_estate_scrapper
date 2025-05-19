from abc import ABC, abstractmethod
from playwright.async_api  import async_playwright
from Helpers.logger import get_logger
import asyncio  
from datetime import datetime

class BaseScraper(ABC):
    def __init__(self, url, cookies_button_selector):
        self.cookies_button_selector = cookies_button_selector
        self.browser = None
        self.page = None
        self.url = url
        self.isSuccess = True
        self.logger = get_logger(self.__class__.__name__)

    async def run_scraper(self):
        # Retry 3 times if the scraper fails
        start = datetime.now()
        for attempt in range(1, 4):
            try:
                async with async_playwright() as p_wright:
                    # Launch the browser
                    await self.open_browser(p_wright)
                    self.page_setup()
                    await self.accept_cookies(self.page)
                    await self.select_city(self.city_name)
                    await self.filter_results()
                    await self.wait_for_element()
                    await self.scrape_offers()
                # RETURN BOOL OR STH TO CHECK IF REALLY COMPLETED BCS NOW IT LOG SUCCES EVEN IF ERROR
                    if self.isSuccess:
                        end = datetime.now()
                        elapsed = end - start
                        self.logger.info(f"Scraping completed successfully for {self.city_name}, time elapsed:{elapsed.total_seconds() / 60:.2f} min. URL: {self.url}")
                        await self.close_browser()

                        break  # Exit the loop if successful
                    else:
                        end = datetime.now()
                        elapsed = end - start
                        self.logger.error(f"Failed after 3 attempts, time elapsed:{elapsed.total_seconds() / 60:.2f} min. URL: {self.url}")
                        
            except Exception as e:
                end = datetime.now()
                elapsed = end - start
                self.logger.error(f"Error in run_scraper (Attempt {attempt}): {e}. URL: {self.url}")
                if attempt == 3: 
                    self.logger.error(f"Failed after 3 attempts, time elapsed:{elapsed.total_seconds() / 60:.2f} min. URL: {self.url}")
                await asyncio.sleep(2)  

    async def open_browser(self, p_wright):
        try:
            self.browser = await p_wright.chromium.launch(headless=False)
            self.page = await self.browser.new_page()
            await self.page.goto(self.url)
        except Exception as e:
            self.logger.error(f"Failed to open browser: {e}. URL: {self.url}")
    
    async def accept_cookies(self, page):
        try:
            await page.locator(f"text={self.cookies_button_selector}").click()
        except Exception as e:
            self.logger.error(f"Failed to accept cookies: {e}. URL: {self.url}")

    async def wait_for_element(self):
        await self.page.wait_for_timeout(1500)  

    async def close_browser(self):
        if self.browser:
            await self.browser.close()
            self.browser = None
        else:
            print("Browser is not open.")
    
    def page_setup(self):
        try:
            self.page.set_default_timeout(30000)
            self.page.set_default_navigation_timeout(30000)
        except Exception as e:
            self.logger.error(f"Failed to set up page: {e}. URL: {self.url}")

    @abstractmethod
    async def select_city(self, city_name):
        """
        Abstract method to select a city on the page.
        Implemented in the derived class.
        """
        pass
    
    @abstractmethod
    async def filter_results(self):
        """
        Abstract method to filter results on the page.
        Implemented in the derived class.
        """
        pass
    
    @abstractmethod
    async def scrape_offers(self):
        """
        Abstract method to scrape offers from the page.
        Implemented in the derived class.
        """
        pass
