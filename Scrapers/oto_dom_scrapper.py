from Scrapers.base_scraper import BaseScraper

class OtoDomScraper(BaseScraper):
    def __init__(self):
        self.url = "https://www.otodom.pl"
        self.cookies_button_selector = "Akceptuję"
        super().__init__(self.url,self.cookies_button_selector)

    async def run_oto_dom_scraper(self):
        await self.run_scraper()

        


