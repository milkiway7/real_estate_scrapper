from abc import ABC, abstractmethod
from playwright.async_api  import async_playwright
from Helpers.logger import get_logger
import asyncio  

class BaseScraper(ABC):
    def __init__(self, url, cookies_button_selector):
        self.cookies_button_selector = cookies_button_selector
        self.browser = None
        self.page = None
        self.url = url
        self.logger = get_logger(self.__class__.__name__)

    async def run_scraper(self):
        # Retry 3 times if the scraper fails
        for attempt in range(1, 4):
            try:
                async with async_playwright() as p_wright:
                    # Launch the browser
                    await self.open_browser(p_wright)
                    self.page_setup()
                    await self.accept_cookies()
                    await self.select_city(self.city_name)
            except Exception as e:
                self.logger.error(f"Error in run_scraper (Attempt {attempt}): {e}. URL: {self.url}")
                if attempt == 3: 
                    self.logger.error(f"Failed after 3 attempts. URL: {self.url}")
                await asyncio.sleep(2)  

    async def open_browser(self, p_wright):
        try:
            self.browser = await p_wright.chromium.launch(headless=False)
            self.page = await self.browser.new_page()
            await self.page.goto(self.url)
        except Exception as e:
            self.logger.error(f"Failed to open browser: {e}. URL: {self.url}")
    
    def page_setup(self):
        try:
            self.page.set_default_timeout(10000)
            self.page.set_default_navigation_timeout(10000)
        except Exception as e:
            self.logger.error(f"Failed to set up page: {e}. URL: {self.url}")
    
    async def accept_cookies(self):
        try:
            await self.page.locator(f"text={self.cookies_button_selector}").click()
        except Exception as e:
            self.logger.error(f"Failed to accept cookies: {e}. URL: {self.url}")

    @abstractmethod
    async def select_city(self, city_name):
        """
        Abstract method to select a city on the page.
        Implemented in the derived class.
        """
        pass


    async def close_browser(self):
        if self.browser:
            await self.browser.close()
            self.browser = None
        else:
            print("Browser is not open.")

