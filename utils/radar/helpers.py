from collections import defaultdict


def group_elements(elements: dict):
    grouped_elements = defaultdict(list)
    for element in elements:
        grouped_elements[element['scrap_element_name']].append(element['scrap_element_xpath'])
    return grouped_elements
