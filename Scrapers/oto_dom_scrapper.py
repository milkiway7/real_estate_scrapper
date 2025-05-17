from Scrapers.base_scraper import BaseScraper
from ScrappersConfiguration.otodom_configuration import OTODOM_CONFIGURATION
from Api.ApiDataStructure.oto_dom_data_structure import otodom_data_structure
class OtoDomScraper(BaseScraper):
    def __init__(self, city_name):
        self.city_name = city_name 
        self.offer_page = None
        self.configuration_selectors = OTODOM_CONFIGURATION["selectors"]
        self.json_data = otodom_data_structure
        super().__init__(OTODOM_CONFIGURATION["url"],OTODOM_CONFIGURATION["cookies_button_selector"])

    async def run_oto_dom_scraper(self):
        await self.run_scraper()

    async def select_city(self, city_name):
        try:
            await self.page.locator(self.configuration_selectors["find_city_button"]).click()
            await self.wait_for_element()
            city_input = self.page.locator(self.configuration_selectors["find_city_input"])
            await city_input.fill(city_name)
            await self.wait_for_element() 
            await city_input.press("Enter")
            await self.page.keyboard.press("Escape")
            await self.wait_for_element() 
            await self.page.locator(self.configuration_selectors["search_button"]).click()
        except Exception as e:
            self.logger.error(f"Failed to select city: {e}. URL: {self.url}")

    async def filter_results(self):
        try:
            container = self.page.locator([self.configuration_selectors["filter_button_container"]])
            dropdown = container.locator(self.configuration_selectors["filter_button"])
            await dropdown.click()
            await self.wait_for_element()
            await self.page.locator(self.configuration_selectors["filter_newest"]).click()
        except Exception as e:
            self.logger.error(f"Failed to filter results: {e}. URL: {self.url}")

    async def scrape_offers(self):
        try:
            next_page_button_is_visible = await self.is_next_page_button_visible()
            while next_page_button_is_visible:
                offers_lists = self.page.locator(self.configuration_selectors["offets_list"])
                lists_count = await offers_lists.count()
                for list in range(lists_count):
                    current_list = offers_lists.nth(list)
                    offers_items = current_list.locator(self.configuration_selectors["offer_container"])
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
                    await self.scrap_data()
                    #close offer_page
                    await self.offer_page.close()
                    #focus on main page with offers list
                    await self.page.bring_to_front()
        except Exception as e:
            self.logger.error(f"Failed to open offer: {e}. URL: {self.url}")
            self.isSuccess = False

    async def is_next_page_button_visible(self):
        try:
            next_button = self.page.locator(self.configuration_selectors["next_page_button"])
            return await next_button.is_visible()
        except Exception as e:
            self.logger.error(f"Failed to check next page button visibility: {e}. URL: {self.url}")
            self.isSuccess = False
        
    async def go_to_next_page(self):
        try:
            next_button = self.page.locator(self)
            if await next_button.is_visible():
                await next_button.scroll_into_view_if_needed()
                await next_button.click()
                await self.wait_for_element()
        except Exception as e:
            self.logger.error(f"Failed to go to next page: {e}. URL: {self.url}")
            self.isSuccess = False

    async def scrap_data(self):
        try:
            # Scrape data from the offer page
            self.json_data["url"] = self.offer_page.url
            self.json_data["title"] = await self.offer_page.locator(OTODOM_CONFIGURATION["selectors"]) # Add the correct selector for title
            self.json_data["address"] = None  # Add the correct selector for address
            self.json_data["price"] = None  # Add the correct selector for price
            self.json_data["offer_type"] = None  # Add the correct selector for offer type
            self.json_data["area"] = None  # Add the correct selector for area
            self.json_data["rooms"] = None  # Add the correct selector for rooms
            self.json_data["heating"] = None  # Add the correct selector for heating
            self.json_data["floor"] = None  # Add the correct selector for floor
            self.json_data["rent"] = None  # Add the correct selector for rent
            self.json_data["building_condition"] = None  # Add the correct selector for building condition
            self.json_data["market"] = None  # Add the correct selector for market
            self.json_data["ownership_form"] = None  # Add the correct selector for ownership form
            self.json_data["available"] = None  # Add the correct selector for available
            self.json_data["additional_info"] = None  # Add the correct selector for additional info
            self.json_data["construction_year"] = None  # Add the correct selector for construction year
            self.json_data["elevator"] = None  # Add the correct selector for elevator
            self.json_data["windows"] = None  # Add the correct selector for windows
            self.json_data["energy_certificate"] = None  # Add the correct selector for energy certificate
            self.json_data["equipment"] = None  # Add the correct selector for equipment
            self.json_data["description"] = None  # Add the correct selector for description
            a = 1
            # Add more fields as needed
        except Exception as e:
            self.logger.error(f"Failed to scrape data: {e}. URL: {self.offer_page.url}")
            self.isSuccess = False