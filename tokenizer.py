import sys


def tokenize(file_path):
    parsed = []
    try:
        with open(file_path, 'r') as file:
            word_builder = ''
            for line in file:
                for c in line:
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
                    word_builder = ''
    except FileNotFoundError:
        print(f"❌ File '{file_path}' not found.")
        sys.exit(1)
    return parsed