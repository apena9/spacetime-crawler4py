import re
import os
from urllib.parse import urlparse, urljoin, urldefrag
from bs4 import BeautifulSoup
from lxml import etree
import tokenizer # "pip install lxml" in terminal



def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

ALLOWED_DOMAINS = [
    "ics.uci.edu",
    "cs.uci.edu",
    "informatics.uci.edu",
    "stat.uci.edu"
]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    compiled_links = []
    if resp.status != 200:
        return compiled_links

    content_type = resp.raw_response.headers.get("Content-Type", "").lower()
    # other acceptable non-html formats --> XML (sitemaps) and plain text (robots.txt)
     # changed parser from "html.parser" to "lxml" to handle both html and xml formats.

    '''
    if "xml" in content_type or "html" in content_type:  # html specifc to avoid images !! just as a quick note for us 
        compiled_links.append() 
        []
    elif "text/plain" in content_type:
        compiled_links.append()
    '''
    if "html" not in content_type:
        return []
    try:
        # other acceptable non-html formats --> XML (sitemaps) and plain text (robots.txt)
        # changed parser from "html.parser" to "lxml" to handle both html and xml formats.


        soup_info = BeautifulSoup(resp.raw_response.content, "lxml") # this is the return of the information which will be paresed in html
        tokenizer(resp) # calling the tokenizer function on our response 
        for id_tag in soup_info.find_all("a", href=True):
            raw_href = id_tag["href"]

            absolute_url = urljoin(resp.url, raw_href)

            clean_url, _ = urldefrag(absolute_url)

            compiled_links.append(clean_url)
        return compiled_links

    except Exception as e:
        print(f"Error extracting links from {url}: {e}")
        return []


def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if not any(domain in parsed.netloc for domain in ALLOWED_DOMAINS):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
'''

Filtering:
- ics open lab + from terminal 
- Honor the politeness delay for each site ✅
- Crawl all pages with high textual information content
- Detect and avoid infinite traps
- Detect and avoid sets of similar pages with no information
- Detect and avoid dead URLs that return a 200 status but no data (click here to see what the different HTTP status codes mean Links to an external site.)
- Detect and avoid crawling very large files, especially if they have low information value
- Filter out invalid domains
- Defragment


- build parser
- report stuff



Functions:
Extract_next_links(url, response) : “crawling” the url
Parse the “response”
Identify URL hyperlinks/report stuff
Add hyperlinks to list
Filtering:
Defragment
Filter out invalid domains
Detect and avoid dead URLs that return a 200 status but no data (click here to see what the different HTTP status codes mean Links to an external site.)


Is_valid(url) : check if link is valid
Filtering:



'''