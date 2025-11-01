import sys
from collections import Counter
from bs4 import BeautifulSoup

def tokenize(text):
    try:
        # Parse the raw HTML/XML content using lxml parser
        soup = BeautifulSoup(text.raw_response.content, "lxml")

        # Remove script and style elements since they don't contain meaningful text
        for tag in soup(["script", "style"]):
            tag.extract()

        text = soup.get_text(separator=' ')
        parsed = []
        word_builder = ''

        # Tokenize the text manually
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

        # Count most common tokens
        counter = Counter(parsed)
        top_50 = counter.most_common(50)

        for i, (word, count) in enumerate(top_50, start=1):
            print(f"{i:2}. {word:<15} {count}")

    except Exception as e:
        print(f"Error found: {e}")

    return parsed  # Return list of tokens
