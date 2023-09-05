# from utils.db.manager import QueryManager
# from utils.enums.radar_table_fields import WebRadarStringsInfo, WebRadarStringsInfoOnDuplicate
# from utils.enums.radar_tables import DatabaseTables
#
# if __name__ == "__main__":
#     # Example usage with BaseUserFields enum
#     query_manager = QueryManager(DatabaseTables.WEB_RADAR_STRINGS_INFO.value,
#                                  WebRadarStringsInfo, WebRadarStringsInfoOnDuplicate)
#
#     # Insert
#     insert_data = {
#         'search_string': 'cold chain monitoring alerts',
#         'internal_website_ref': 'innovation99-coldchain',
#         'website_url': 'https://search.yahoo.com/',
#         'result_url': 'https://www.cognizant.com/us/en/glossary/cold-chain-monitoring',
#         'page_rank': '1',
#         'seo_keywords': '{"meta": null, "title": "%(search_string\')s www.cognizant.com", "header1": "", "header2": "", "keywords": null}',
#         'date': '2023-08-30 18:35:19.487754'
#     }
#
#     query_manager.insert_on_duplicate_key_update(insert_data)
from process_layer.radar.execute import execute_radar

execute_radar()