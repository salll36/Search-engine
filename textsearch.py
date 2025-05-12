from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import jieba
import math
import os


class TextSearch:
    def __init__(self, folder_path, keywords, k):
        self.folder_path = folder_path
        self.keywords = keywords
        self.k = k

    def fenci(self, s):
        seg_list = jieba.cut(s)
        result = []
        for seg in seg_list:
            seg = "".join(seg.split())
            if seg != '，' and seg != '？' and seg != '。' and seg != "\n" and seg != "\n\n" and seg != '':
                result.append(seg)
        return result

    def proceed(self, texts):
        docs = []
        for text in texts:
            doc = self.fenci(text)
            docs.append(doc)
        return docs

    def tf(self, docs):
        tf_word = []
        for i, doc in enumerate(docs):
            doc_count = len(doc)
            tf = {}
            for p in doc:
                if p in tf:
                    tf[p] += 1.0 * 1 / doc_count
                else:
                    tf[p] = 1.0 * 1 / doc_count
            tf_word.append(tf)
        return tf_word

    def idf(self, docs):
        word2df = {}
        for i, doc in enumerate(docs):
            for word in doc:
                if word in word2df:
                    word2df[word].append(i)
                else:
                    word2df[word] = []
                    word2df[word].append(i)
        for key in word2df:
            word2df[key] = len(set(word2df[key]))

        idf_word = {}
        docs_count = len(docs)
        for word in word2df:
            idf_word[word] = math.log(docs_count / (word2df[word] + 1))

        return idf_word

    def tf_idf(self, tf_word, idf_word):
        result = []
        for i, p in enumerate(tf_word):
            tfidf_word = {}
            for key in p:
                tfidf_word[key] = tf_word[i][key] * idf_word[key]
            result.append(tfidf_word)

        return result

    def BF(self, arr, target, index):
        for i in range(len(arr)):
            sum = 0
            for j in range(len(target)):
                if i + j < len(arr) and target[j] == arr[i + j]:
                    sum += 1
            if sum == len(target):
                index.append(i)

    def shingle(self, content, index_list, k):
        result_list = []
        for index in index_list:
            result_list.append(content[index:index + k])
        return result_list

    def search(self):
        content_list = []
        index_list = []
        for p in os.listdir(self.folder_path):
            name = self.folder_path + '/' + p
            with open(name, "r", encoding="utf-8") as f:
                content_list.append(f.read())

        ''' 1-计算TF-IDF '''
        docs = self.proceed(content_list)
        tf_word = self.tf(docs)
        idf_word = self.idf(docs)
        tf_idf = self.tf_idf(tf_word, idf_word)

        ''' 2-BF算法匹配下标 '''
        for content in content_list:
            mylist = []
            for p in self.keywords:
                self.BF(content, p, mylist)
            mylist.sort()
            index_list.append(mylist)

        ''' 3-shingle算法设置窗口大小 '''
        for n, content in enumerate(content_list):
            result_list = self.shingle(content, index_list[n], self.k)
            for i, result in enumerate(result_list):
                weight = 0
                for p in self.keywords:
                    index = []
                    self.BF(result, p, index)
                    weight += tf_idf[n][p] * len(index)
