from utils import get_logger
from urllib.parse import urlparse
from scraper import ALLOWED_DOMAINS

subdomains = dict() # string, int key value pairs (url, count)
subdomains_logger = get_logger('Subdomains')

def update_subdomains(scraped_urls):
    '''
    uses scraped_urls and marks the urls that it has seen.
    '''
    for scraped_url in scraped_urls:
        domain = urlparse(scraped_url).hostname
        if domain and not (domain in ALLOWED_DOMAINS):
            try:
                subdomains[domain] += 1
                #subdomains_logger.info(f"UPDATING COUNT: '{full_subdomain}': {subdomains[full_subdomain]} occurences")
            except KeyError:
                subdomains[domain] = 1
                #subdomains_logger.info(f"NEW SUBDOMAIN: '{full_subdomain}'")

def get_total_subdomains():
    '''
    writes out subdomain and its count. Called after crawl is completed.
    sorted from most occuring subdomains to least occuring.
    '''
    sorted_subdomains = sorted(subdomains.items(), key=lambda item: item[1])
    for item in sorted_subdomains:
        subdomains_logger.info(
                f"Subdomain: {item[0]} --> {item[1]}")
        
