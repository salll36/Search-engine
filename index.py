from flask import Flask
from flask import render_template
from flask import request
from spider import search
from textsearch import TextSearch
from flask_cors import cross_origin
from search import retrieval
import jieba
from Pinyin2Hanzi import DefaultDagParams
from Pinyin2Hanzi import dag

# 参数可以加载指定的文件夹里的静态文件，把静态文件也指定到templates里，如css,js静态资源的加载
app = Flask(__name__,static_url_path='', static_folder='templates', template_folder='templates')

''' 装饰器-给函数新增功能 '''

# 入口
@app.route("/")
def index():
    return render_template("index.html")

# 爬虫接口
@app.route("/spider",methods=["POST"])
@cross_origin()
def index_spider():
    # 如果输入是拼音
    print(request)
    if request.get_json()["key"].replace(" ","").encode('utf-8').isalpha():
        lists = request.get_json()["key"].split(" ")
        dagParams = DefaultDagParams()
        myresult = dag(dagParams, lists, path_num=10, log=True)
        print(myresult[0].path)
        keywords = jieba.cut(myresult[0].path[0])
        text_search = TextSearch('./', keywords, 120)
        to_retrieval = retrieval(myresult[0].path[0])
        result = to_retrieval.jiansuo()
    # 否则输入的是汉字
    else:
        # search(request.get_json()["key"])
        keywords = jieba.cut(request.get_json()["key"])
        text_search = TextSearch('./', keywords, 120)
        to_retrieval = retrieval(request.get_json()["key"])
        result = to_retrieval.jiansuo()

    return result

app.run(host='0.0.0.0',port=5000,debug=True) # 代码修改后自动重启项目