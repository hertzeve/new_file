from nltk.stem import WordNetLemmatizer
import string
from nltk.tokenize import sent_tokenize
from search_system.python_code import query_process

def highlight_one(article,search_query):
    str = ''
    le = WordNetLemmatizer()
    table = str.maketrans('', '', string.punctuation)
    sentences = sent_tokenize(article.content)
    keyword = le.lemmatize(search_query.lower().translate(table))
    for sentence in sentences:
        list = sentence.split(" ")
        for word in list:
            word_lem = le.lemmatize(word.lower().translate(table))
            if word_lem == keyword:
                str = str + " " + "<strong><font color=red>" + word + "</font></strong>"
            else:
                str = str + " " + word
    return str

def highlight_andor(article,search_query):
    str = ''
    le = WordNetLemmatizer()
    sentences = sent_tokenize(article.content)
    keywords = query_process.lemmatizing(search_query)
    for sentence in sentences:
        list = sentence.split(" ")
        for word in list:
            table = str.maketrans('', '', string.punctuation)
            word_lem = le.lemmatize(word.lower().translate(table))
            if word_lem == keywords[0]:
                str = str + " " + "<strong><font color=red>" + word + "</font></strong>"
            elif word_lem == keywords[2]:
                str = str + " " + "<strong><font color=red>" + word + "</font></strong>"
            else:
                str = str + " " + word
    return str

def highlight_phrase(article,search_query):
    str = ''
    le = WordNetLemmatizer()
    sentences = sent_tokenize(article.content)
    keywords = query_process.lemmatizing(search_query)
    for sentence in sentences:
        i = 0
        n=0
        list = sentence.split(" ")
        lem_list = query_process.lemmatizing(sentence)
        for keyword in keywords:
            if keyword in lem_list:
                n+=1
        if n == len(keywords):
            for word in list:
                table = str.maketrans('', '', string.punctuation)
                word_lem = le.lemmatize(word.lower().translate(table))
                if word_lem in keywords:
                    str = str + " " + "<strong><font color=red>" + word + "</font></strong>"
                else:
                    str = str + " " + word
        else:
            str = str + " " + sentence
    return str

def highlight_rankPhrase(article,search_query):
    str = ''
    le = WordNetLemmatizer()
    sentences = sent_tokenize(article.content)
    keywords = query_process.lemmatizing(search_query)
    for sentence in sentences:
        list = sentence.split(" ")
        for word in list:
            table = str.maketrans('', '', string.punctuation)
            word_lem = le.lemmatize(word.lower().translate(table))
            if word_lem in keywords:
                str = str + " " + "<strong><font color=red>" + word + "</font></strong>"
            else:
                str = str + " " + word
    return str