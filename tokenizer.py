from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import KrovetzStemmer

def tokenize(text):
    """
    Tokenizes a single string of text, ignores common English stopwords,
    and applies Krovetz stemming.
    """
    try:
        stemmer = KrovetzStemmer()
        stop_words = set(stopwords.words('english'))  # English stopword list
        parsed = []
        word_builder = ''

        # Loop through every character in the string
        for c in text:
            if c == "'" or c == "-" or c.isalnum():
                word_builder += c
            else:
                if word_builder.endswith("'s"):
                    word_builder = word_builder[:-2]
                if word_builder and word_builder.isascii():
                    token = word_builder.lower()
                    if token not in stop_words:
                        parsed.append(token)
                word_builder = ''

        # Handle last token if text ends with a word
        if word_builder:
            if word_builder.endswith("'s"):
                word_builder = word_builder[:-2]
            if word_builder and word_builder.isascii():
                token = word_builder.lower()
                if token not in stop_words:
                    parsed.append(token)

        # Apply Krovetz stemming
        stemmed = [stemmer.stem(word) for word in parsed]

        # Count most common tokens
        counter = Counter(stemmed)
        top_50 = counter.most_common(50)

        for i, (word, count) in enumerate(top_50, start=1):
            print(f"{i:2}. {word:<15} {count}")

        return stemmed

    except Exception as e:
        print(f"Error in tokenize: {e}")
        return []
