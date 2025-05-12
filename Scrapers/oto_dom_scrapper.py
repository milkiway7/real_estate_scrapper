from Scrapers.base_scraper import BaseScraper
from ScrappersConfiguration.otodom_configuration import OTODOM_CONFIGURATION
class OtoDomScraper(BaseScraper):
    def __init__(self, city_name):
        self.city_name = city_name 
        super().__init__(OTODOM_CONFIGURATION["url"],OTODOM_CONFIGURATION["cookies_button_selector"])

    async def run_oto_dom_scraper(self):
        await self.run_scraper()

    async def select_city(self, city_name):
        try:
            await self.page.locator(OTODOM_CONFIGURATION["selectors"]["find_city_button"]).click()
            city_input = self.page.locator(OTODOM_CONFIGURATION["selectors"]["find_city_input"])
            await city_input.fill(city_name)
            await city_input.press("Enter")
        except Exception as e:
            self.logger.error(f"Failed to select city: {e}. URL: {self.url}")

        


