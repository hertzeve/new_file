import os
import re
import json
from filecmp import cmp

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import string
from collections import OrderedDict





dic_map = {}# 储存文件名及对应的单词

path_files = "../data"  # 相对路径
files = os.listdir(path_files)  # 读取文件夹中所有的文件名
dic_map = dict(zip(range(len(files)), files)) #id:1,2,3


# def lemmatizing_sent(sentence):
#     lemmatizer = WordNetLemmatizer()
#     stem_words2 = []
#     wordsSplit = word_tokenize(sentence)
#     for w in wordsSplit:
#         stem_words2.append(lemmatizer.lemmatize(w))
#     return stem_words2
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


# def tokenizing(str):
#     WORD_RE = re.compile(r'\W+')  # 正则化
#     words = WORD_RE.split(str.lower())
#     print(words)
#     return words


def a_doc_word_location(text):
        """
        Split a text in words. Returns a list of tuple that contains
        (word, location) location is the starting words position of the word.
        alse do the job of normalization
        """
        new_text = []
        new_text = lemmatizing(text)
        # print(new_text)
        word_list = []
        wcurrent = []
        windex = 0
        # enumerate can get the index and the specific content of a string
        for i, c in enumerate(new_text):

            word_list.append((i, c))# 一个文章中的 i:在文本中的位置（数字）; c:单词

        return word_list

def inverted_index(text):
        """
        Create an Inverted-Index of the specified text document.
            {word:[locations]}
        """
        inverted = {}

        for index, word in a_doc_word_location(text):
            # setdefault func is similar with the func get,but it can add new key and set default value to the dic when the key does not exist
            locations = inverted.setdefault(word, [])
            locations.append(index)

        return inverted

def inverted_index_add(inverted, doc_id, doc_index):
        """
        Add Invertd-Index doc_index of the document doc_id to the
        Multi-Document Inverted-Index (inverted),
        using doc_id as document identifier.
            {word:{doc_id:[locations]}}
        """
        for word, locations in doc_index.items():

            indices = inverted.setdefault(word, {})
            indices[doc_id] = locations
        return inverted

# 读取所有文件，并为所有单词建立文档索引
def create_index():
    inverted = {}
    path_files = "../data"  # 相对路径
    files = os.listdir(path_files)  # 读取文件夹中所有的文件名
    dic_map = dict(zip(range(len(files)), files))  # id:1,2,3
    documents = {}
    for id, document in dic_map.items():
    # 把文件内容读出存放到 article 中
        f = open(path_files + "/" + document)  # ../data/filenanme
        iter_f = iter(f)
        content = ""
        for line in iter_f:  # 遍历文件，一行行遍历，读取文本
            content = content + line
        documents[id] = content

    for doc_id, text in documents.items():
        doc_index = inverted_index(text)
        inverted = inverted_index_add(inverted, doc_id, doc_index)
    return inverted


# 把索引写入 index
def write_index_file(index):
    js = json.dumps(index)
    file = open('../../index.txt', 'w', encoding='utf-8')
    file.write(js)
    file.close()
    print("成功建立！")
