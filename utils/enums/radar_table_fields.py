from enum import Enum


class WebRadarWebsites(Enum):
    WEBSITE_URL = 'website_url'
    LOAD_MORE_XPATH = 'loadmore_xpath'
    NEXT_CLICK_XPATH = 'next_click_xpath'
    LINK_XPATH = 'link_xpath'
    SEARCHBAR_XPATH = "searchbar_xpath"


class WebRadarStings(Enum):
    SEARCH_STRING = 'search_string'
    INTERNAL_WEBSITE_REF = 'internal_website_ref'


class WebRadarStringsInfo(Enum):
    SEARCH_STRING = "search_string"
    INTERNAL_WEBSITE_REF = "internal_website_ref"
    WEBSITE_URL = "website_url"
    RESULT_URL = "result_url"
    PAGE_RANK = "page_rank"
    SEO_KEYWORDS = "seo_keywords"
    DATE = "date"


class WebRadarStringsInfoOnDuplicate(Enum):
    PAGE_RANK = "page_rank"
    SEO_KEYWORDS = "seo_keywords"
    DATE = "date"


class WebRadarStringsError(Enum):
    WEB_URL = "web_url"
    ERROR_SHORT = "error_short"
    ERROR_LONG = "error_long"
    SEARCH_STRING = "search_string"
    ERROR_TIMESTAMP = "error_timestamp"


class WebRadarScrapElements(Enum):
    SCRAP_ELEMENT_NAME = "scrap_element_name"
    SCRAP_ELEMENT_XPATH = "scrap_element_xpath"
