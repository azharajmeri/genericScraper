from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebDriverManager:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.driver = None

    def start_driver(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path)

    def navigate_to(self, url):
        self.driver.get(url)

    def wait_for_element(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutError:
            print(f"Element {locator} not found within {timeout} seconds.")

    def click_element(self, locator):
        element = self.find_element(locator)
        if element:
            element.click()

    def switch_to_new_window(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def refresh_driver(self):
        if self.driver:
            self.driver.quit()
        self.start_driver()

    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def scroll_to_bottom(self, max_iterations=5):
        initial_height = self.driver.execute_script("return document.body.scrollHeight")
        for _ in range(max_iterations):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(self.driver, 5).until(
                lambda driver: driver.execute_script("return document.body.scrollHeight") > initial_height)
            initial_height = self.driver.execute_script("return document.body.scrollHeight")

        # Check if the page content has actually changed
        final_height = self.driver.execute_script("return document.body.scrollHeight")
        if final_height == initial_height:
            print("Page content did not change after scrolling.")
        else:
            print("Page content has changed after scrolling.")

    def find_element(self, locator):
        try:
            return self.driver.find_element(*locator)
        except NoSuchElementException:
            return None

    def find_elements(self, locator):
        try:
            return self.driver.find_elements(*locator)
        except NoSuchElementException:
            return []
