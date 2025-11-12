import json
import os
from nltk.corpus import stopwords # pip install nltk
from krovetzstemmer import Stemmer # pip install krovetzstemmer


def print_tokens(token_frequencies: dict[str, int], file_obj):
    token_sorted = sorted(token_frequencies.items(), key=lambda item:item[1], reverse=True)
    for item in token_sorted:
        print(f"<{item[0]}> => <{item[1]}>", file=file_obj)

def compute_word_frequencies(token_list: list[str], token_frequencies: dict):
    '''
    Takes a list of strings (represents the list of tokens from a single page.
    Modifies the dictionary (of all page words)  
    '''
    for token in token_list:
        try:
            token_frequencies[token] += 1
        except KeyError:
            token_frequencies[token] = 1

def valid_tokens(tokens:list[str]):
    '''
    Takes a list of tokens and determines if it should be counted (for longest_page mainly)
    '''
    for token in tokens:
        if len(token) > 1:
            return True
    return False

def tokenize(text):
    """
    Tokenizes the text of a single file (soup.get_text).
    Takes in a string of the entire text from the file, returns a list of string representing tokens of the page
    """
    try:
        stemmer = Stemmer()
        stop_words = set(stopwords.words('english'))
        tokens = []
        word_builder = ''

        for c in text:
            if c == "'" or c == "-" or c.isalnum():
                word_builder += c
            else:
                if word_builder.endswith("'s"):
                    word_builder = word_builder[:-2]
                if word_builder and word_builder.isascii():
                    token = word_builder.lower()
                    if token not in stop_words:
                        stemmed = stemmer.stem(token)
                        tokens.append(stemmed)
                word_builder = ''

            # handle last token per page
        if word_builder:
            if word_builder.endswith("'s"):
                word_builder = word_builder[:-2]
            if word_builder and word_builder.isascii():
                token = word_builder.lower()
                if token not in stop_words:
                    stemmed = stemmer.stem(token)
                    tokens.append(stemmed)

        return tokens

    except Exception as e:
        print(f"Error in tokenize: {e}")
        return {}
def build_inverted_index(folder):
    I = defaultdict(list)  #  HashTable set up like seen in notes
    n = 0 # starting at 0 for docs being parsed 

    for root, dirs, files in os.walk(folder):
        for filename in files:
            if not filename.endswith(".json"):
                continue

            n += 1  # count document to keep track of where each token came from
            path = os.path.join(root, filename) #simply just getting the pathj for folders !

            try:
                with open(path, "r", encoding="utf-8") as f:
                    doc = json.load(f) # using load will allow us to easily parse and use information back
                text = doc.get("content", "") # will try and grab anything labled within content // may need to update and debug as "content"
                # ... appears elsewhere too
                if not text:
                    continue

                T = tokenize(text)  # ← Parse(d)
                token_freq = {}
                for t in T:
                    token_freq[t] = token_freq.get(t, 0) + 1  # count tf

                # For each token, update postings
                for t, tf in token_freq.items():
                    posting = {"doc_id": path, "tf": tf}
                    I[t].append(posting)

            except Exception as e:
                print(f"Error processing {e}")

    return I  # ← return I
