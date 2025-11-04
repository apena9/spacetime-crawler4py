
import re
from urllib.parse import urlparse, urljoin, urldefrag

from subdomains import update_subdomains
from collections import namedtuple

from bs4 import BeautifulSoup
from lxml import etree # "pip install lxml" in terminal
import tokenizer


TRAPS = [ #list of strings representing keywords that indicate a trap
    'wics.ics.uci.edu',
    '/events',
    'isg.ics.uci.edu/event',
    'doku.php',
    'ics.uci.edu/~eppstein/pix',
    'physics.uci.edu',
    'cecs.uci.edu',
    'grape.ics.uci.edj/wiki/public/timeline',
    'login.php'
]
'''
calendar,
ical,
tribe,
'''

def scraper(url, resp):
    links = extract_next_links(url, resp)
    scraped_urls = [link for link in links if is_valid(link)]
    update_subdomains(scraped_urls)
    return scraped_urls


MIN_HTML_BYTES = 64
MIN_VISIBLE_WORDS = 8

Page = namedtuple("Page",['url','word_count','tokens'])
longest_page = Page(url = "", word_count = 0, tokens = [])
all_word_frequencies = dict()

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
    global longest_page
    global all_word_frequencies
    compiled_links = []
    if resp.status != 200:
        return compiled_links
    
    content_type = resp.raw_response.headers.get("Content-Type", "").lower()
    content_bytes = resp.raw_response.content or b""
     
     #Dead URL: HTTP 200 but tiny/empty body
    if len(content_bytes) < MIN_HTML_BYTES or ("html" not in content_type):
        return compiled_links
    # ====== HTML ======== 
    try:
        soup_info = BeautifulSoup(resp.raw_response.content, "lxml") # this is the return of the information which will be paresed in html
        
        visible_text = soup_info.get_text(strip=True) 
        tokens = tokenizer.tokenize(visible_text)

        this_page = Page(url = url, word_count = len(tokens), tokens=tokens)
        longest_page = this_page if (this_page.word_count > longest_page.word_count) else longest_page # els: no-op
        
        tokenizer.compute_word_frequencies(tokens, all_word_frequencies)

        if len(tokens) < MIN_VISIBLE_WORDS: # treat as dead/empty HTML page
            return []
        
        for id_tag in soup_info.find_all("a", href=True): # this would be only difference between pages.
            raw_href = id_tag["href"]

            absolute_url = urljoin(resp.url, raw_href)

            clean_url, _ = urldefrag(absolute_url)

            compiled_links.append(clean_url)

        seen = set()
        deduped = []
        for u in compiled_links:
            if u not in seen:
                seen.add(u)
                deduped.append(u)
        return deduped
    
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
        if not is_valid_domain(parsed.hostname): # check if domain is valid
            return False
        if is_trap(url):# check for traps
            return False
        if is_duplicate(parsed):
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
    
ALLOWED_DOMAINS = [
    "ics.uci.edu",
    "cs.uci.edu",
    "informatics.uci.edu",
    "stat.uci.edu"
]
def is_valid_domain(url : str) -> bool:
    global ALLOWED_DOMAINS
    if isinstance(url, type(None)):
        return False
    for domain in ALLOWED_DOMAINS:
        if domain in url: # when URL is NONE
            return True
    return False

def is_trap(url: str) -> bool: # DETECT_TRAP
    '''
    rules:

    if path depth exceeds 15
    '''
    for trap in TRAPS:
        if trap in url:
            return True
    return False

duplicate_paths = set()
DUPLICATES = [
    'grape.ics.uci.ed/wiki/public/wiki'
]
def is_duplicate(parsed_url) -> bool: #duplicates hueristically
    global duplicate_paths
    global DUPLICATES
    string_url = f'{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}'
    for duplicate in DUPLICATES:
        if duplicate in string_url:
            if string_url in duplicate_paths:
                return True
            else:
                duplicate_paths.add(string_url)
                return False
    return False



'''

Filtering:
- ics open lab + from terminal 
- Honor the politeness delay for each site 
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