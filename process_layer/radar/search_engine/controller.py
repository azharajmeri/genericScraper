from selenium.common import ElementNotInteractableException, WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from process_layer.radar.database.controller import DatabaseController
from utils.enums.radar_table_fields import WebRadarWebsites, WebRadarStings
from utils.radar import settings
from utils.radar.exceptions import UnableToInteractWithSearchBox, UnableToLocateSearchBox, UnableToRenderPage
from utils.selenium.manager import WebDriverManager


class EngineController:
    def __init__(self, search_string_details, search_engine_details, seo_elements, scrape_count):
        self.driver_manager = WebDriverManager(settings.DRIVER_PATH)
        self.driver_manager.start_driver()
        self.search_string_details = search_string_details
        self.search_engine_details = search_engine_details
        self.seo_elements = seo_elements
        self.scrape_count = scrape_count
        self.links_to_scrape = []
        self.last_scrape_links = []
        self.next_page_click_count = 0

    def initiate(self):
        print(f"INITIATED: {self.search_engine_details.get(WebRadarWebsites.WEBSITE_URL.value)} - FOR: {self.search_string_details.get(WebRadarStings.SEARCH_STRING.value)}")
        self.driver_manager.navigate_to(self.search_engine_details.get(WebRadarWebsites.WEBSITE_URL.value), raise_exception=True)
        self.initiate_link_scraping()
        self.driver_manager.close_driver()

    def initiate_link_scraping(self):
        self.input_search_string()
        self.extract_all_links()
        self.scrape_pages()

    def input_search_string(self):
        print(f"INPUTTING SEARCH STRING: {self.search_string_details.get(WebRadarStings.SEARCH_STRING.value)}")
        if not (search_box := self.driver_manager.find_element_with_wait((By.XPATH, self.search_engine_details.get(WebRadarWebsites.SEARCHBAR_XPATH.value)), 30)):
            raise UnableToLocateSearchBox
        try:
            search_box.clear()
            search_box.send_keys(self.search_string_details.get(WebRadarStings.SEARCH_STRING.value))
            search_box.send_keys(Keys.ENTER)
        except ElementNotInteractableException:
            raise UnableToInteractWithSearchBox
        except Exception:
            raise UnableToInteractWithSearchBox

    def extract_all_links(self):
        print(f"EXTRACTING LINKS FROM: {self.search_engine_details.get(WebRadarWebsites.WEBSITE_URL.value)}")
        try:
            while not self.check_count_target_reached():
                if self.next_page_click_count > 4:
                    DatabaseController(self.search_string_details, self.search_engine_details).store_error("Might be switching between same pages.",
                        f"Unable to extract {self.scrape_count} links from {self.driver_manager.driver.current_url}, switching between same pages.")
                    break
                self.extract_with_dynamic_content()
                self.links_to_scrape.extend(self.last_scrape_links)
                if not self.go_to_next_page():
                    if not self.check_count_target_reached():
                        DatabaseController(self.search_string_details, self.search_engine_details).store_error("No next button found.", f"Unable to extract {self.scrape_count} links from {self.search_engine_details.get(WebRadarWebsites.WEBSITE_URL.value)}.")
                    break
        except Exception as e:
            DatabaseController(self.search_string_details, self.search_engine_details).store_error(
                "Unable to extract all links.",
                f"Unable to extract {self.scrape_count} links from {self.driver_manager.driver.current_url}. - ERROR: {e}")

    def extract_with_dynamic_content(self):
        try:
            height_change = True
            while height_change:
                height_change = self.driver_manager.scroll_to_bottom()

                if self.check_count_target_reached():
                    break

                if load_more_xpath := self.search_engine_details.get(WebRadarWebsites.LOAD_MORE_XPATH.value):
                    if load_more_button := self.driver_manager.find_element_with_wait((By.XPATH, load_more_xpath)):
                        load_more_button.click()
        except Exception as e:
            DatabaseController(self.search_string_details, self.search_engine_details).store_error(
                "Unable to extract dynamic content.",
                f"Unable to extract {self.scrape_count} links from {self.driver_manager.driver.current_url}. - ERROR: {e}")

    def go_to_next_page(self):
        try:
            self.next_page_click_count += 1
            if next_page_xpath := self.search_engine_details.get(WebRadarWebsites.NEXT_CLICK_XPATH.value):
                if next_page_button := self.driver_manager.find_element_with_wait((By.XPATH, next_page_xpath)):
                    next_page_button.click()
                    return True
        except Exception as e:
            DatabaseController(self.search_string_details, self.search_engine_details).store_error(
                "Next button not intractable.",
                f"Unable to click next button - ERROR {e}.")
        return False

    def check_count_target_reached(self):
        return self.get_links_count() + len(self.links_to_scrape) >= self.scrape_count

    def get_links(self):
        links_elements = self.driver_manager.find_elements_with_wait(
            (By.XPATH, self.search_engine_details.get(WebRadarWebsites.LINK_XPATH.value)))
        self.last_scrape_links = [a.get_attribute('href') for a in links_elements]
        return links_elements

    def get_links_count(self):
        return len(self.get_links())

    def scrape_pages(self):
        print("STARTING LINK'S META DATA EXTRACTION")
        for rank, page in enumerate(self.links_to_scrape[:self.scrape_count], start=1):
            print(f"DRIVER RENDERING PAGE: {page} - RANK: {rank}")
            try:
                self.driver_manager.open_new_tab(page, raise_exception=True)
            except UnableToRenderPage:
                DatabaseController(self.search_string_details, self.search_engine_details).store_error("Search Engine links failed to render, taking too long to get rendered.",
                    f"Unable to render page for URL {page}")
                continue
            except Exception as e:
                DatabaseController(self.search_string_details, self.search_engine_details).store_error(
                    "Search Engine links failed to render.",
                    f"Unable to render page for URL {page}")
                continue
            self.extract_seo_keywords(rank, page)
            self.driver_manager.close_current_tab()

    def extract_seo_keywords(self, rank, page):
        print(f"EXTRACTING KEYWORDS FROM: {page} - RANK: {rank}")
        try:
            self.store_record(
                {
                    "keywords": {element: self.extract_keyword(element, element_xpath_list, page) for element, element_xpath_list in self.seo_elements.items()},
                    "rank": rank,
                    "page_url": page
                }
            )
        except WebDriverException as e:
            DatabaseController(self.search_string_details, self.search_engine_details).store_error(
                "Unable to extract SEO keywords.", f"PAGE: {page} - ERROR: {e}")
        except Exception as e:
            DatabaseController(self.search_string_details, self.search_engine_details).store_error(
                "Unable to extract SEO keywords.", f"PAGE: {page} - ERROR: {e}")

    def extract_keyword(self, element, element_xpath_list, page):
        try:
            for xpath in element_xpath_list:
                if keyword := self.driver_manager.find_element_with_wait((By.XPATH, xpath)):
                    if data := keyword.get_attribute("content"):
                        return data
                    if data := keyword.get_attribute("innerText"):
                        return data
        except Exception as e:
            DatabaseController(self.search_string_details, self.search_engine_details).store_error(
                "Unable to extract SEO keyword.", f"KEYWORD: {element} - PAGE: {page} - ERROR: {e}")

    def store_record(self, record):
        DatabaseController(self.search_string_details, self.search_engine_details).store_information(record)
