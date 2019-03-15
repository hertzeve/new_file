from nltk.stem import WordNetLemmatizer
import string


def do_split(text):
    # split into words by white space
    words = text.split()
    # convert to lower case
    words = [word.lower() for word in words]
    # remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in words]
    # print(stripped)
    return stripped
#lemmatizing
def lemmatizing(text):
    # lemmatizing
    le_words = []
    le = WordNetLemmatizer()
    wordsSplit = do_split(text)

    for w in wordsSplit:
        le_words.append(le.lemmatize(w))
    # print(le_words)
    return le_words




