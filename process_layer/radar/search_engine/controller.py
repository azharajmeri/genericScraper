import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

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
        self.extracted_data = []

    def initiate(self):
        self.driver_manager.navigate_to(self.search_engine_details.get(WebRadarWebsites.WEBSITE_URL.value))
        self.initiate_link_scraping()
        self.driver_manager.close_driver()

    def initiate_link_scraping(self):
        self.input_search_string()
        self.scrape_links()

    def input_search_string(self):
        search_box = self.driver_manager.find_element((By.XPATH, self.search_engine_details.get(WebRadarWebsites.SEARCHBAR_XPATH.value)))
        search_box.clear()
        search_box.send_keys(self.search_string_details.get(WebRadarStings.SEARCH_STRING.value))
        search_box.send_keys(Keys.ENTER)

    def scrape_links(self):
        links_elements = self.driver_manager.find_elements_with_wait((By.XPATH, self.search_engine_details.get(WebRadarWebsites.LINK_XPATH.value)))
        self.scrape_pages([a.get_attribute('href') for a in links_elements])

    def scrape_pages(self, pages):
        for page in pages:
            self.driver_manager.open_new_tab(page)
            time.sleep(2)
            self.driver_manager.close_current_tab()
