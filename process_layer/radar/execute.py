from process_layer.radar.database.controller import DatabaseController
from process_layer.radar.search_engine.controller import EngineController
from utils.radar.exceptions import UnableToRenderPage, UnableToInteractWithSearchBox, UnableToLocateSearchBox
from utils.radar.helpers import group_elements
from utils.selenium.initiate_managers import web_radar_scrap_elements_manager, web_radar_strings_manager, \
    web_radar_search_engine_manager


def initiate_data_extraction(search_string_details, search_engine_details, seo_elements):
    try:
        results = EngineController(search_string_details, search_engine_details, seo_elements).initiate()
    except UnableToRenderPage as e:
        DatabaseController(search_string_details, search_engine_details).store_error("Home page rendering fail.", e.message)
        return
    except UnableToLocateSearchBox as e:
        DatabaseController(search_string_details, search_engine_details).store_error("Search Box not found.", e.message)
        return
    except UnableToInteractWithSearchBox as e:
        DatabaseController(search_string_details, search_engine_details).store_error("Search Box not Interactive.", e.message)
        return
    DatabaseController(search_string_details, search_engine_details).store_information(results)


def execute_radar():
    grouped_seo_elements = group_elements(web_radar_scrap_elements_manager.read_all())
    for search_string in web_radar_strings_manager.read_all():
        for search_engine in web_radar_search_engine_manager.read_all():
            initiate_data_extraction(search_string, search_engine, grouped_seo_elements)
        break
