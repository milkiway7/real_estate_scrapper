from Scrapers.base_scraper import BaseScraper
from ScrappersConfiguration.otodom_configuration import OTODOM_CONFIGURATION
class OtoDomScraper(BaseScraper):
    def __init__(self, city_name):
        self.city_name = city_name 
        self.offer_page = None
        super().__init__(OTODOM_CONFIGURATION["url"],OTODOM_CONFIGURATION["cookies_button_selector"])

    async def run_oto_dom_scraper(self):
        await self.run_scraper()

    async def select_city(self, city_name):
        try:
            await self.page.locator(OTODOM_CONFIGURATION["selectors"]["find_city_button"]).click()
            await self.wait_for_element()
            city_input = self.page.locator(OTODOM_CONFIGURATION["selectors"]["find_city_input"])
            await city_input.fill(city_name)
            await self.wait_for_element() 
            await city_input.press("Enter")
            await self.page.keyboard.press("Escape")
            await self.wait_for_element() 
            await self.page.locator(OTODOM_CONFIGURATION["selectors"]["search_button"]).click()
        except Exception as e:
            self.logger.error(f"Failed to select city: {e}. URL: {self.url}")

    async def filter_results(self):
        try:
            container = self.page.locator('[data-sentry-component="DropdownSorting"]')
            dropdown = container.locator('[data-cy="dropdown"]')
            await dropdown.click()
            await self.wait_for_element()
            await self.page.locator(OTODOM_CONFIGURATION["selectors"]["filter_newest"]).click()
        except Exception as e:
            self.logger.error(f"Failed to filter results: {e}. URL: {self.url}")

    async def scrape_offers(self):
        try:
            next_page_button_is_visible = await self.is_next_page_button_visible()
            while next_page_button_is_visible:
                offers_lists = self.page.locator(OTODOM_CONFIGURATION["selectors"]["offets_list"])
                lists_count = await offers_lists.count()
                for list in range(lists_count):
                    current_list = offers_lists.nth(list)
                    offers_items = current_list.locator('li article[data-cy="listing-item"] section')
                    await self.open_offers(offers_items)
                    next_page_button_is_visible = await self.is_next_page_button_visible()
                    if not next_page_button_is_visible:
                        break
                    if list == lists_count - 1:
                        await self.go_to_next_page()
        except Exception as e:
            self.logger.error(f"Failed to run offers scrape loop: {e}. URL: {self.url}")

        
    async def open_offers(self, offers_items):
        try:
            offers_count = await offers_items.count()
            for offer_index in range(offers_count):
                offer = offers_items.nth(offer_index)
                anchor = offer.locator("a").first
                if await anchor.is_visible():
                    await offer.scroll_into_view_if_needed()
                    href = await anchor.first.get_attribute("href")
                    self.offer_page = await self.browser.new_page()
                    await self.offer_page.goto(self.url + href)
                    await self.accept_cookies(self.offer_page)
                    # scrapp data
                    #close offer_page
                    await self.offer_page.close()
                    #focus on main page with offers list
                    await self.page.bring_to_front()
        except Exception as e:
            self.logger.error(f"Failed to open offer: {e}. URL: {self.url}")
            self.isSuccess = False

    async def is_next_page_button_visible(self):
        try:
            next_button = self.page.locator("li[title='Go to next Page']")
            return await next_button.is_visible()
        except Exception as e:
            self.logger.error(f"Failed to check next page button visibility: {e}. URL: {self.url}")
            self.isSuccess = False
        
    async def go_to_next_page(self):
        try:
            next_button = self.page.locator("li[title='Go to next Page']")
            if await next_button.is_visible():
                await next_button.scroll_into_view_if_needed()
                await next_button.click()
                await self.wait_for_element()
        except Exception as e:
            self.logger.error(f"Failed to go to next page: {e}. URL: {self.url}")
            self.isSuccess = False

