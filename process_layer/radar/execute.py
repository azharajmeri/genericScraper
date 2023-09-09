from process_layer.radar.database.controller import DatabaseController
from process_layer.radar.search_engine.controller import EngineController
from utils.db.manager import QueryManager
from utils.enums.radar_table_fields import (WebRadarStings, WebRadarWebsites,
                                            WebRadarScrapElements, WebRadarStringsInfo,
                                            WebRadarStringsInfoOnDuplicate)
from utils.enums.radar_tables import DatabaseTables
from utils.radar.helpers import group_elements

web_radar_string_info_manager = QueryManager(DatabaseTables.WEB_RADAR_STRINGS_INFO.value,
                                             WebRadarStringsInfo, WebRadarStringsInfoOnDuplicate)


def initiate_data_extraction(search_string_details, search_engine_details, seo_elements):
    results = EngineController(search_string_details, search_engine_details, seo_elements).initiate()
    DatabaseController(web_radar_string_info_manager, search_string_details, search_engine_details).store_information(results)


def execute_radar():
    web_radar_strings_manager = QueryManager(DatabaseTables.WEB_RADAR_STRINGS.value, WebRadarStings)
    web_radar_search_engine_manager = QueryManager(DatabaseTables.WEB_RADAR_WEBSITES.value, WebRadarWebsites)
    web_radar_scrap_elements_manager = QueryManager(DatabaseTables.WEB_RADAR_SCRAP_ELEMENTS.value, WebRadarScrapElements)

    grouped_seo_elements = group_elements(web_radar_scrap_elements_manager.read_all())
    for search_string in web_radar_strings_manager.read_all():
        for search_engine in web_radar_search_engine_manager.read_all():
            initiate_data_extraction(search_string, search_engine, grouped_seo_elements)
            break
        break
