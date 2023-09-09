from collections import defaultdict

from utils.enums.radar_table_fields import WebRadarScrapElements


def group_elements(elements: dict):
    grouped_elements = defaultdict(list)
    for element in elements:
        grouped_elements[element[WebRadarScrapElements.SCRAP_ELEMENT_NAME.value]].append(element[WebRadarScrapElements.SCRAP_ELEMENT_XPATH.value])
    return grouped_elements
