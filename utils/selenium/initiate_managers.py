from utils.db.manager import QueryManager
from utils.enums.radar_table_fields import (WebRadarStringsInfo, WebRadarStringsInfoOnDuplicate,
                                            WebRadarStringsErrorOnDuplicate, WebRadarStings,
                                            WebRadarWebsites, WebRadarScrapElements, WebRadarStringsError)
from utils.enums.radar_tables import DatabaseTables

web_radar_string_info_manager = QueryManager(DatabaseTables.WEB_RADAR_STRINGS_INFO.value, WebRadarStringsInfo,
                                             WebRadarStringsInfoOnDuplicate)
web_radar_string_error_manager = QueryManager(DatabaseTables.WEB_RADAR_STRINGS_ERROR.value, WebRadarStringsError,
                                              WebRadarStringsErrorOnDuplicate)
web_radar_strings_manager = QueryManager(DatabaseTables.WEB_RADAR_STRINGS.value, WebRadarStings)
web_radar_search_engine_manager = QueryManager(DatabaseTables.WEB_RADAR_WEBSITES.value, WebRadarWebsites)
web_radar_scrap_elements_manager = QueryManager(DatabaseTables.WEB_RADAR_SCRAP_ELEMENTS.value, WebRadarScrapElements)
