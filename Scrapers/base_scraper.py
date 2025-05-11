from abc import ABC, abstractmethod
from playwright.async_api  import async_playwright
from Helpers.logger import get_logger

class BaseScraper(ABC):
    def __init__(self, url, cookies_button_selector):
        self.cookies_button_selector = cookies_button_selector
        self.browser = None
        self.page = None
        self.url = url
        self.logger = get_logger(self.__class__.__name__)

    async def run_scraper(self):
        try:
            async with async_playwright() as p_wright:
                # Launch the browser
                await self.open_browser(p_wright)
                await self.page_setup()
                await self.accept_cookies()
        except Exception as e:
            self.logger.error(f"Error in run_scraper: {e}. URL: {self.url}")

    async def open_browser(self, p_wright):
        try:
            self.browser = await p_wright.chromium.launch(headless=False)
            self.page = await self.browser.new_page()
            await self.page.goto(self.url)
        except Exception as e:
            self.logger.error(f"Failed to open browser: {e}. URL: {self.url}")
    
    async def page_setup(self):
        try:
            await self.page.set_default_timeout(10000)
            await self.page.set_default_navigation_timeout(10000)
        except Exception as e:
            self.logger.error(f"Failed to set up page: {e}. URL: {self.url}")
    
    async def accept_cookies(self):
        try:
            await self.page.locator(f"text={self.cookies_button_selector}").click()
        except Exception as e:
            self.logger.error(f"Failed to accept cookies: {e}. URL: {self.url}")

    async def select_city(self, city_locator):
        try:
            await self.page.locator(city_locator).click()
            await self.page.wait_for_timeout(2000)  # Wait for the city selection to take effect

    async def close_browser(self):
        if self.browser:
            await self.browser.close()
            self.browser = None
        else:
            print("Browser is not open.")

