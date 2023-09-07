from utils.selenium.manager import WebDriverManager


class WebPageHandler:
    def __init__(self, path=None):
        self.driver_manager = WebDriverManager(path)
        self.driver_manager.start_driver()
