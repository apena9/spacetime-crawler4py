import sys
from collections import Counter

from bs4 import BeautifulSoup
import nltk
from nltk.stem import KrovetzStemmer
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)
STOPWRDS = set(stopwords.words('english'))
stemmer = KrovetzStemmer()

def tokenize(text):
    try:
       soup = BeautifulSoup(text.raw_response.content, "lxml")
       for tag in soup(["script", "style"]):  
            tag.extract()
       text = soup.get_text(separator=' ')
       parsed = []
       word_builder = ''
       for c in text:
            if c == "'" or c == "-" or c.isalnum():
                word_builder += c
            else:
                if word_builder.endswith("'s"):
                    word_builder = word_builder[:-2]
                if word_builder and word_builder.isascii():
                    parsed.append(word_builder.lower())
                word_builder = ''
       if word_builder:
            if word_builder.endswith("'s"):
                word_builder = word_builder[:-2]
            if word_builder and word_builder.isascii():
                parsed.append(word_builder.lower())


            parsed_info = [t for t in parsed if t not in STOPWRDS and len(t) > 1]
            stemmed_tokens = [stemmer.stem(t) for t in parsed_info]
            counter = Counter(stemmed_tokens)
            top_50 = counter.most_common(50)
    except FileNotFoundError:
        print(f" File '{file_path}' not found.")
        sys.exit(1)
    return parsed