# Radar

### Project Description: 

Project collects links from various search engines. After, the script proceeds to extract specific elements from the web pages corresponding to those links. The extraction process is structured, targeting elements as defined in a predefined table. This enables the retrieval of specific.

### NOTE!
The **.env** file is pushed because community version of prefect doesn't have the Database credential block.


## Table Description

* web_radarwebsites50
    ```text
    Contains search engines details, URLs and elements path.
    ```
  
* web_radarstrings51
    ```text
    Contains search strings which are pasted in the search boxes
    of search engines.
    ```
  
* web_radar_scrap_elements54
    ```text
    Contains the element which are needed to be scraped from the links which 
    appear on search engine result like header, title, meta, .etc.
    ```
  
* web_radarstringsinfo52
    ```text
    Contains the final result of scraping from the details fetched from the above tables.
    Contains the output of elements mentioned in the table `web_radar_scrap_elements54`.
    ```
  
* web_radarstringserror53
    ```text
    Obvious from the name, stores error logs.
    ```
  


**SQL UPDATES**

```sql
ALTER TABLE web_radarstringsinfo52 ADD CONSTRAINT `UK_table_search_string_website_url_result_url` UNIQUE (search_string, website_url, result_url);
```
 
```sql
ALTER TABLE web_radarstringserror53 ADD CONSTRAINT `UK_table_web_url_error_short_search_string` UNIQUE (web_url, error_short, search_string);
```
