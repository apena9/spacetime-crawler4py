from urllib.parse import urlparse

ALLOWED_DOMAINS = [
    "ics.uci.edu",
    "cs.uci.edu",
    "informatics.uci.edu",
    "stat.uci.edu"
]

subdomains = dict() # string, int key value pairs (url, count)
# way to print subdomains to a separate file.

def update_subdomains(scraped_urls):
    '''
    uses scraped_urls and marks the urls that it has seen.
    '''
    for scraped_url in scraped_urls:
        domain = urlparse(scraped_url).hostname
        if domain and not (domain in ALLOWED_DOMAINS):
            try:
                subdomains[domain] += 1
            except KeyError:
                subdomains[domain] = 1

def print_subdomains(file_obj):
    '''
    writes out subdomain and its count. Called after crawl is completed.
    sorted from most occuring subdomains to least occuring.
    '''
    sorted_subdomains = sorted(subdomains.items(), key=lambda item: item[1],reverse=True)
    for item in sorted_subdomains:
        print(f"Subdomain: {item[0]} --> {item[1]}", file=file_obj)
        
