from nltk.corpus import stopwords
from nltk.stem import KrovetzStemmer

def tokenize(all_texts):
    """
    Tokenizes and stems words across ALL crawled pages.
    Builds a dictionary {word: frequency} for all pages combined.
    Prints the top 50 most common words overall.
    """
    try:
        stemmer = KrovetzStemmer()
        stop_words = set(stopwords.words('english'))
        word_freq = {}  # dictionary to store word counts

        for text in all_texts:  # loop through all crawled pages
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
                            word_freq[stemmed] = word_freq.get(stemmed, 0) + 1
                    word_builder = ''

            # handle last token per page
            if word_builder:
                if word_builder.endswith("'s"):
                    word_builder = word_builder[:-2]
                if word_builder and word_builder.isascii():
                    token = word_builder.lower()
                    if token not in stop_words:
                        stemmed = stemmer.stem(token)
                        word_freq[stemmed] = word_freq.get(stemmed, 0) + 1

        # sort by frequency in descending order
        top_50 = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:50]

        for i, (word, count) in enumerate(top_50, start=1):
            print(f"{i:2}. {word:<15} {count}")

        return word_freq

    except Exception as e:
        print(f"Error in tokenize: {e}")
        return {}
