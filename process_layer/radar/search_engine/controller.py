import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from utils.enums.radar_table_fields import WebRadarWebsites, WebRadarStings, WebRadarScrapElements
from utils.selenium.manager import WebDriverManager


class EngineController:
    def __init__(self, search_string_details, search_engine_details, seo_elements, scrape_count=40):
        self.driver_manager = WebDriverManager("/home/root349/Projects/chromedriver/chromedriver")
        self.driver_manager.start_driver()
        self.search_string_details = search_string_details
        self.search_engine_details = search_engine_details
        self.seo_elements = seo_elements
        self.scrape_count = scrape_count
        self.links_to_scrape = []
        self.last_scrape_links = []

    def initiate(self):
        self.driver_manager.navigate_to(self.search_engine_details.get(WebRadarWebsites.WEBSITE_URL.value))
        self.initiate_link_scraping()
        self.driver_manager.close_driver()

    def initiate_link_scraping(self):
        self.input_search_string()
        self.extract_all_links()
        self.scrape_pages()

    def input_search_string(self):
        search_box = self.driver_manager.find_element((By.XPATH, self.search_engine_details.get(WebRadarWebsites.SEARCHBAR_XPATH.value)))
        search_box.clear()
        search_box.send_keys(self.search_string_details.get(WebRadarStings.SEARCH_STRING.value))
        search_box.send_keys(Keys.ENTER)

    def extract_all_links(self):
        while not self.check_count_target_reached():
            self.extract_with_dynamic_content()
            self.links_to_scrape.extend(self.last_scrape_links)
            if not self.go_to_next_page():
                break

        # Todo: Remove below comments
        print(self.links_to_scrape)
        print("LENGTH:", len(self.links_to_scrape))

    def extract_with_dynamic_content(self):
        height_change = True
        while height_change:
            height_change = self.driver_manager.scroll_to_bottom()

            if self.check_count_target_reached():
                break

            if load_more_xpath := self.search_engine_details.get(WebRadarWebsites.LOAD_MORE_XPATH.value):
                if load_more_button := self.driver_manager.find_element_with_wait((By.XPATH, load_more_xpath)):
                    load_more_button.click()

    def go_to_next_page(self):
        if next_page_xpath := self.search_engine_details.get(WebRadarWebsites.NEXT_CLICK_XPATH.value):
            if next_page_button := self.driver_manager.find_element_with_wait((By.XPATH, next_page_xpath)):
                next_page_button.click()
                return True
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
        for page in self.links_to_scrape:
            self.driver_manager.open_new_tab(page)
            # Todo: Continue from here, scrape SEO keywords from page
            self.driver_manager.close_current_tab()
