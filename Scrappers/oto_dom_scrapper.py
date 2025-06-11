from Scrappers.base_scraper import BaseScraper
from ScrappersConfiguration.otodom_configuration import OTODOM_CONFIGURATION
from Api.send_data_client import SendDataClient


class OtoDomScraper(BaseScraper):
    def __init__(self, city_name):
        self.city_name = city_name 
        self.offer_page = None
        self.configuration_selectors = OTODOM_CONFIGURATION["selectors"]
        self.configuration_offert_selectors = OTODOM_CONFIGURATION["selectors"]["offert"]
        self.json_data = None
        self.send_data_client = SendDataClient()
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
            self.isSuccess = False

    async def filter_results(self):
        try:
            container = self.page.locator('[data-sentry-component="DropdownSorting"]')
            dropdown = container.locator('[data-cy="dropdown"]')
            await dropdown.click()
            await self.wait_for_element()
            await self.page.locator(self.configuration_selectors["filter_newest"]).click(timeout=5000)
        except Exception as e:
            self.logger.error(f"Failed to filter results: {e}. URL: {self.url}")
            self.isSuccess = False

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
            self.isSuccess = False
        
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
                    await self.scrap_data()
                    await self.offer_page.close()
                    if len(self.offers) >= 2:
                        await self.send_data_client.send_data_to_analysis(self.offers)
                        self.offers.clear()
                    self.offers.append(self.json_data)
                    await self.page.bring_to_front()
        except Exception as e:
            self.logger.error(f"Failed to open offer: {e}. URL: {self.url}")
            
    async def is_next_page_button_visible(self):
        try:
            next_button = self.page.locator(self.configuration_selectors["next_page_button"])
            return await next_button.is_visible()
        except Exception as e:
            self.logger.error(f"Failed to check next page button visibility: {e}. URL: {self.url}")
        
    async def go_to_next_page(self):
        try:
            next_button = self.page.locator(self.configuration_selectors["next_page_button"])
            if await next_button.is_visible():
                await next_button.scroll_into_view_if_needed()
                await next_button.click()
                await self.wait_for_element()
        except Exception as e:
            self.logger.error(f"Failed to go to next page: {e}. URL: {self.url}")

    async def scrap_data(self):
        try:
            # Scrape data from the offer page
            self.json_data = {
                "url": self.offer_page.url,
                "title": await self.offer_page.locator(self.configuration_offert_selectors["title"]).inner_text(),
                "address": await self.offer_page.locator(self.configuration_offert_selectors["address"]).inner_text(),
                "price": await self.offer_page.locator(self.configuration_offert_selectors["price"]).inner_text(),
                "price_per_m2": await self.offer_page.locator(self.configuration_offert_selectors["price_per_m2"]).inner_text(),
                # "construction_year": "",
                # "elevator": "",
                # "windows": "",
                # "energy_certificate": "",
                # "equipment": "",
                "description": await self.get_description(),
            }
            # ADD COMPANY IF EXSIST
            
            await self.get_details_info()
            # Add more fields as needed
        except Exception as e:
            self.logger.error(f"Failed to scrape data: {e}. URL: {self.offer_page.url}")

    async def get_details_info(self):
        try:
            for detail in self.configuration_offert_selectors["details_table"]:
                detail_value_label = self.offer_page.locator("p", has_text=self.configuration_offert_selectors["details_table"][detail])
                detail_value = await detail_value_label.locator("xpath=following-sibling::p[1]").first.inner_text()
                self.json_data[detail] = detail_value
        except Exception as e:
            self.logger.error(f"Failed to get details info: {e}. URL: {self.offer_page.url}")
    
    async def get_description(self):
        try:
            description =  await self.offer_page.locator("div[data-cy='adPageAdDescription']").inner_text()
            return description
        except Exception as e:
            self.logger.error(f"Failed to get description: {e}. URL: {self.offer_page.url}")
    
