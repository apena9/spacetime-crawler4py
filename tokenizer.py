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

        # sort by frequency in descending order
        # top_50 = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:50]

        # for i, (word, count) in enumerate(top_50, start=1):
        #     print(f"{i:2}. {word:<15} {count}")

        return tokens

    except Exception as e:
        print(f"Error in tokenize: {e}")
        return {}
