import contextlib
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from utils.radar.exceptions import UnableToRenderPage


class WebDriverManager:
    def __init__(self, driver_path):
        self.options = Options()
        self.dc = DesiredCapabilities().CHROME
        self.dc["pageLoadStrategy"] = "normal"
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--enable-popup-blocking")
        self.options.add_argument("enable-automation")
        self.options.add_argument("--disable-browser-side-navigation")
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-dev-tools")
        self.options.add_argument("--window-size=1920x1080")
        self.options.add_argument("--ignore-ssl-errors=yes")
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--single-process")
        self.options.add_argument("log-level=3")
        self.options.add_argument("--allow-insecure-localhost")
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--allow-running-insecure-content")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--remote-debugging-port=9515")
        if not driver_path:
            self.service = Service(ChromeDriverManager().install(), options=self.options, desired_capabilities=self.dc)
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

    def navigate_to(self, url, raise_exception=False):
        if not self.driver:
            self.start_driver()
        try:
            self.driver.get(url)
        except TimeoutException:
            if raise_exception:
                raise UnableToRenderPage

    def open_new_tab(self, url=None, raise_exception=False):
        if self.driver:
            self.driver.execute_script("window.open('', '_blank');")
            self.switch_to_new_window()
        else:
            self.start_driver()
        if url:
            self.navigate_to(url, raise_exception=raise_exception)

    def switch_to_new_window(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def close_current_tab(self):
        self.driver.close()
        self.switch_to_new_window()

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def find_element_with_wait(self, locator):
        try:
            return WebDriverWait(self.driver, 5).until(
                lambda x: x.find_element(
                    *locator
                )
            )
        except TimeoutException as e:
            return None

    def find_elements_with_wait(self, locator):
        try:
            return WebDriverWait(self.driver, 5).until(
                lambda x: x.find_elements(
                    *locator
                )
            )
        except TimeoutException as e:
            return []

    def scroll_to_bottom(self, max_iterations=5):
        SCROLL_COMMAND = "return document.body.scrollHeight"
        next_height = initial_height = self.driver.execute_script(SCROLL_COMMAND)
        for _ in range(max_iterations):
            with contextlib.suppress(TimeoutException):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                WebDriverWait(self.driver, 1).until(
                    lambda driver: driver.execute_script(SCROLL_COMMAND) > next_height)
            next_height = self.driver.execute_script(SCROLL_COMMAND)

        # Check if the page content has actually changed
        final_height = self.driver.execute_script(SCROLL_COMMAND)
        return final_height != initial_height
