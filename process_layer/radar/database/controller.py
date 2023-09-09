import json
from datetime import datetime

from utils.enums.radar_table_fields import WebRadarStringsInfo, WebRadarStings, WebRadarWebsites


class DatabaseController:
    def __init__(self, web_radar_string_info_manager, search_string_details, search_engine_details):
        self.web_radar_string_info_manager = web_radar_string_info_manager
        self.search_string_details = search_string_details
        self.search_engine_details = search_engine_details

    def store_information(self, results):
        for result in results:
            self.web_radar_string_info_manager.insert_on_duplicate_key_update({
                WebRadarStringsInfo.SEARCH_STRING.value: self.search_string_details.get(WebRadarStings.SEARCH_STRING.value),
                WebRadarStringsInfo.INTERNAL_WEBSITE_REF.value: self.search_string_details.get(
                    WebRadarStings.INTERNAL_WEBSITE_REF.value),
                WebRadarStringsInfo.WEBSITE_URL.value: self.search_engine_details.get(WebRadarWebsites.WEBSITE_URL.value),
                WebRadarStringsInfo.RESULT_URL.value: result.get("page_url"),
                WebRadarStringsInfo.PAGE_RANK.value: result.get("rank"),
                WebRadarStringsInfo.SEO_KEYWORDS.value: json.dumps(result.get("keywords")),
                WebRadarStringsInfo.DATE.value: datetime.now(),
            })