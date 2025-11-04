import os

from tokenizer import print_tokens
from subdomains import print_subdomains, subdomains
import scraper # for longest page and most common 50 words (which are updated over-time)


directory = 'Report'
# makes a 

scraper.all_word_frequencies



def make_directory(directory: str):
    # creates a director where files information containing information for report are located
    files = ['top_50.txt', 'longest_page.txt', 'subdomains.txt']
    os.makedirs(directory, exist_ok=True)
    for name in files:
        path = os.path.join(directory,name)
        open(path, mode="w").close()

def report_all(directory: str):
    '''writes desired information about crawled pages into a text file.
    'top_50.txt', 'longest_page.txt', and 'subdomains.txt' with respective information
    '''
    make_directory(directory)
    for f in os.listdir(directory):
        full_path = os.path.join(directory,f)
        if f == 'top_50.txt':
            with open(full_path, mode= 'w') as file_obj:
                print_tokens(scraper.all_word_frequencies, file_obj)
        elif f == 'longest_page.txt':
            with open(full_path, mode='w') as file_obj:
                url, word_count,tokens = scraper.longest_page.url, scraper.longest_page.word_count, scraper.longest_page.tokens
                print(f'{url}\nWord Count: {word_count}\n{tokens}', file=file_obj)
        elif f == 'subdomains.txt':
            with open(full_path, mode='w') as file_obj:
                print_subdomains(file_obj)
