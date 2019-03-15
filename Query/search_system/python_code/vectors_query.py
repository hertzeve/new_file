from gensim import corpora,models,similarities
from collections import defaultdict
import os
import string
from nltk.stem import WordNetLemmatizer




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

#去掉enlish.stop的stopwords
def rem_stopwords(stripped):
    stopwords = []
    path = "../english.stop"
    file = open(path)
    iter_f = iter(file)
    str = ""
    for line in iter_f:  # 遍历文件，一行行遍历，读取文本
        str = str + line
    stopword = str.split()
    stopwords.append(stopword)
    wordlist = []
    for word in stripped:
        if word not in stopwords:
            wordlist.append(word)
    return wordlist

#lemmatizing
def lemmatizing(wordlist):
    # lemmatizing
    le_words = []
    le = WordNetLemmatizer()
    for w in wordlist:
        le_words.append(le.lemmatize(w))
    # print(le_words)
    return le_words

#计算词频
def cal_tf(wordslist):
    frequency=defaultdict(int)   # 构建一个字典对象
    for text in wordslist:           #遍历分词后的结果集，计算每个词的频率
        for token in text:
            frequency[token]+=1
    print(frequency)


def vector_query(wordslist,lem_query):

    # 创建字典-单词与编号之间的映射
    dictionary = corpora.Dictionary(wordslist)  # 生成字典
    dictionary.save('../tfidfdict.dict')
    corpus = [dictionary.doc2bow(text) for text in wordslist]

    tfidf = models.TfidfModel(corpus)
    # 将整个语料库转化成tfidf表示方法
    corpus_tfidf = tfidf[corpus]
    index = similarities.MatrixSimilarity(corpus_tfidf)

    com_doc = dictionary.doc2bow(lem_query)
    # 8,相似度计算
    com_doc_tfidf = tfidf[com_doc]
    # print(com_doc_tfidf)
    sims = index[com_doc_tfidf]

    sims = sorted(enumerate(sims), key=lambda item: -item[1], reverse=False)
    new_sims = []
    for i, c in sims:
        if (c > 0):
            new_sims.append(i)
    return new_sims

def main(lem_query):
    # 读取文本，用一个列表储存起来
    wordslist = []
    path_files = "../data"  # 相对路径
    files = os.listdir(path_files)  # 读取文件夹中所有的文件名
    for file in files:
        f = open(path_files + "/" + file)  # ../data/filenanme
        iter_f = iter(f)
        content = ""
        for line in iter_f:  # 遍历文件，一行行遍历，读取文本
            content = content + line
        split_content = do_split(content)
        re_stopword = rem_stopwords(split_content)
        lem_words = lemmatizing(re_stopword)
        wordslist.append(lem_words)
    cal_tf(wordslist)

    ids = vector_query(wordslist,lem_query)

    return ids