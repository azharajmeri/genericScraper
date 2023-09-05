from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.selenium.manager import WebDriverManager


class WebPageHandler:
    def __init__(self, driver_path):
        self.driver_manager = WebDriverManager(driver_path)
        self.driver_manager.start_driver()
        self.opened_tabs = []  # To store the handles of opened tabs

    def navigate_to_page(self, url):
        self.driver_manager.navigate_to(url)
        self.opened_tabs.append(self.driver_manager.driver.current_window_handle)

    def switch_to_tab(self, tab_index):
        if tab_index < len(self.opened_tabs):
            self.driver_manager.driver.switch_to.window(self.opened_tabs[tab_index])

    def get_current_tab_index(self):
        return self.opened_tabs.index(self.driver_manager.driver.current_window_handle)

    def get_number_of_tabs(self):
        return len(self.opened_tabs)

    def close_current_tab(self):
        current_tab_handle = self.driver_manager.driver.current_window_handle
        if current_tab_handle in self.opened_tabs:
            self.driver_manager.driver.close()
            self.opened_tabs.remove(current_tab_handle)

    def open_new_tab(self, url=None):
        self.driver_manager.driver.execute_script("window.open('', '_blank');")
        new_tab_handle = self.driver_manager.driver.window_handles[-1]  # Get the handle of the newly opened tab
        self.driver_manager.driver.switch_to.window(new_tab_handle)  # Switch to the newly opened tab
        self.opened_tabs.append(new_tab_handle)  # Add the new tab handle to the list
        if url:
            self.navigate_to_page(url)

    def wait_for_element_to_appear(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver_manager.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutError:
            print(f"Element {locator} did not appear within {timeout} seconds.")

    def find_element(self, locator):
        return self.driver_manager.driver.find_element(*locator)

    def find_elements(self, locator):
        return self.driver_manager.driver.find_elements(*locator)
