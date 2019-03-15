import re
import json
from search_system.python_code import query_process



# 考虑到查询操作需要多次执行，把 index 作为全局变量，否则 search_index() 需要传递
# index 参数, document_map 同
index = {}
document_map = {}

# 从position.txt文件中读取索引创建索引字典
def create_index(file_name):
    inverted_index = {}
    file = open('../index.txt', 'r')
    js = file.read()
    inverted_index = json.loads(js)
    print(inverted_index)
    file.close()
    return inverted_index

# 在索引字典中搜索 keywords
# 因为输入查询的格式已经约定所以使用了下标的方法获得数据
def search_index(search_query):
    ids = []
    ids_dic = {}
    keywords = query_process.lemmatizing(search_query)
    if len(keywords) > 1:
        if keywords[1] == 'and':
            #and 操作符
            firstIndexList = []
            secondIndexList = []
            if index.get(keywords[0]) is not None:
                for indexes in index.get(keywords[0]):
                    firstIndexList.append(indexes)
            if index.get(keywords[2]) is not None:
                for indexes in index.get(keywords[2]):
                    secondIndexList.append(indexes)
            ids = list(set(firstIndexList).intersection(set(secondIndexList)))
            return get_result(ids,2)
        elif keywords[1] == 'or':
            #or操作符
            firstIndexList = []
            secondIndexList = []
            if index.get(keywords[0]) is not None:
                for indexes in index.get(keywords[0]):
                    firstIndexList.append(indexes)
            if index.get(keywords[2]) is not None:
                for indexes in index.get(keywords[2]):
                    secondIndexList.append(indexes)
            ids = list(set(firstIndexList).union(set(secondIndexList)))
            return get_result(ids, 2)
        else:
            #短语搜索
            position_compare = {}
            i=1
            intersect_location = []
            for keyword in keywords:
                if keyword not in index.keys():
                    return get_result(ids, 3)
            if index.get(keywords[0]) is not None:
                intersect_docID = (index.get(keywords[0])).keys()
            for term in keywords[1:]:
                print(index.get(keywords[i]))
                intersect_docID = list(set(intersect_docID).intersection(set((index.get(term)).keys())))
            if len(intersect_docID) == 0:
                ids=[]
            else:
                dict = (index.get(keywords[0]))
                for docID in intersect_docID:
                    i = 0
                    intersect_location = dict[docID]
                    for term in keywords[1:]:
                        i += 1
                        dict_another = (index.get(term))
                        another_location = []
                        for number in dict_another[docID]:
                            another_location.append(number - i)  # 将每个位置数值减一，以便用于交集对比
                        intersect_location = list(set(intersect_location).intersection(set(another_location)))
                    if len(intersect_location)>0:
                        ids.append(docID)

            return get_result(ids, 3)
    else:
        #单一单词搜索
        indexlist=[]
        if keywords[0] not in index.keys():
            return get_result(ids, 1)
        else:
            for indexes in index.get(keywords[0]):
                indexlist.append(indexes)
            ids = indexlist
            return get_result(ids,1)


# 输出结果函数
def get_result(ids,identify):
    if (len(ids) == 0):
        return None,0
    else:
        return ids, identify


def main(keywords):
    # 从文件中读取索引创建索引字典用于查询
    global index
    index = create_index('../index.txt')

    # 构造匹配规则
    # pattern = re.compile(r'^([0-9a-zA-Z\-\_]+)(\s+)?((and|or)(\s+)?([0-9a-zA-Z\_\-]+))?$')
    # pattern = re.compile(r'^(\S+)(\s+)?((and|or)(\s+)?(\S+))?$')
    i = 0
    while (i==0):
        result, indentify = search_index(keywords)
        i+=1
    return result,indentify