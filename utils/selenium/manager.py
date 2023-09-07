from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverManager:
    def __init__(self, driver_path):
        if driver_path:
            self.service = Service(ChromeDriverManager().install())
        else:
            self.service = Service(executable_path=driver_path)
        self.driver = None

    def start_driver(self):
        self.driver = webdriver.Chrome(service=self.service)

    def refresh_driver(self):
        if self.driver:
            self.driver.quit()
        self.start_driver()

    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def navigate_to(self, url):
        self.driver.get(url)

    def open_new_tab(self, url=None):
        self.driver.execute_script("window.open('', '_blank');")
        self.switch_to_new_window()
        if url:
            self.navigate_to(url)

    def switch_to_new_window(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def close_current_tab(self):
        self.driver.close()
        self.switch_to_new_window()

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def find_elements_with_wait(self, locator):
        try:
            return WebDriverWait(self.driver, 20).until(
                lambda x: x.find_elements(
                    *locator
                )
            )
        except TimeoutException as e:
            return []
