from prefect import task

from process_layer.radar.database.controller import DatabaseController
from process_layer.radar.search_engine.controller import EngineController
from utils.enums.radar_table_fields import WebRadarWebsites, WebRadarStings
from utils.radar import settings
from utils.radar.exceptions import UnableToRenderPage, UnableToInteractWithSearchBox, UnableToLocateSearchBox
from utils.radar.helpers import group_elements
from utils.selenium.initiate_managers import web_radar_scrap_elements_manager, web_radar_strings_manager, \
    web_radar_search_engine_manager


def initiate_data_extraction(search_string_details, search_engine_details, seo_elements):
    try:
        EngineController(search_string_details, search_engine_details, seo_elements, settings.RADAR_SCRAPE_COUNT).initiate()
    except UnableToRenderPage as e:
        DatabaseController(search_string_details, search_engine_details).store_error("Home page rendering fail.", e.message)
    except UnableToLocateSearchBox as e:
        DatabaseController(search_string_details, search_engine_details).store_error("Search Box not found.", e.message)
    except UnableToInteractWithSearchBox as e:
        DatabaseController(search_string_details, search_engine_details).store_error("Search Box not Interactive.", e.message)
    except Exception as e:
        DatabaseController(search_string_details, search_engine_details).store_error("Unknown exception occured.", e.message)
    print(f"ENDED: {search_engine_details.get(WebRadarWebsites.WEBSITE_URL.value)} - FOR: {search_string_details.get(WebRadarStings.SEARCH_STRING.value)}")


# @task
def execute_radar():
    print("RADAR PROCESS STARTED")
    grouped_seo_elements = group_elements(web_radar_scrap_elements_manager.read_all())
    for search_string in web_radar_strings_manager.read_all():
        for search_engine in web_radar_search_engine_manager.read_all():
            initiate_data_extraction(search_string, search_engine, grouped_seo_elements)
