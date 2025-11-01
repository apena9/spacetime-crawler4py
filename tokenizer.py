import sys
from collections import Counter

from bs4 import BeautifulSoup
import nltk
from nltk.stem import KrovetzStemmer
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)
STOPWRDS = set(stopwords.words('english'))
stemmer = KrovetzStemmer() # making use of the stemmer taught in class

def tokenize(text):
    try:
       
    #Parse the raw HTML/XML content using lxml parser
       soup = BeautifulSoup(text.raw_response.content, "lxml")

       for tag in soup(["script", "style"]):  # Remove script and style elements since they don't contain meaningful text
            tag.extract()
       text = soup.get_text(separator=' ')
       parsed = []
       word_builder = ''
       for c in text:
            if c == "'" or c == "-" or c.isalnum():
                word_builder += c # Add valid characters (letters, numbers, apostrophes, or hyphens) to the current word
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
            # Apply Krovetz stemming
            stemmed_tokens = [stemmer.stem(t) for t in parsed_info]
            counter = Counter(stemmed_tokens)
            top_50 = counter.most_common(50)
            for i, (word, count) in enumerate(top_50, start=1):
                print(f"{i:2}. {word:<15} {count}")


    except Exception as e:
        print(f"Error found {e}")
    return parsed #return a list of the elements