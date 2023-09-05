from utils.enums.radar_table_fields import WebRadarWebsites, WebRadarStings, WebRadarScrapElements


class EngineController:
    def __init__(self, search_string_details, search_engine_details, seo_elements):
        self.search_string_details = search_string_details
        self.search_engine_details = search_engine_details
        self.seo_elements = seo_elements
        self.extracted_data = []

    def scrape(self, url):
        try:
            # Store the scraped data in the controller's data attribute
            self.extracted_data.append()

            return True  # Scraping successful
        except Exception as e:
            print(f"Error while scraping: {str(e)}")
            return False  # Scraping failed

    def store_data(self):
        try:
            return True  # Storage successful
        except Exception as e:
            print(f"Error while storing data: {str(e)}")
            return False  # Storage failed

    def initiate(self):
        pass