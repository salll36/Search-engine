from msedge.selenium_tools import Edge
from msedge.selenium_tools import EdgeOptions
import time
import urllib.parse
from multiprocessing.dummy import Pool # 多进程库
import lxml.html

#实现无可视化界面操作
options = EdgeOptions()
#使用谷歌内核，（至于为什么没有edge内核，我在库里找不到相关代码）
options.use_chromium = True
#这里和谷歌浏览器不一样的是我们不需要加入--，在headless和disable-gpu前面
options.add_argument('headless')
options.add_argument('disable-gpu')
#实现规避检测
options.add_argument('--disable-blink-features=AutomationControlled')





def one_page(mytuble):
    # 实例化浏览器对象,替代了原来的实例化浏览器对象
    driver = Edge(executable_path=r"D:\Python\pycharm编译软件\msedgedriver.exe", options=options)
    url = "https://fsoufsou.com/search?q="+ urllib.parse.quote(mytuble[0]) + "&tbn=all&pageIndex=" + str(mytuble[1])
    driver.get(url)
    time.sleep(0.5)
    result = []
    selector = lxml.html.fromstring(driver.page_source)
    a_list = selector.xpath('//div[@class="flex-row-center"]/a/@href')
    title_list = selector.xpath('//a[@class="title title-text-pc-color"]/text()')
    text_list = []
    not_processed_text = selector.xpath('//div[@class="snippet-container"]/div')
    for p in not_processed_text:
        text_list.append(p.xpath('string(.)').strip())
    for i in range(len(a_list)):
        result.append({
            "href": a_list[i],
            "title": title_list[i],
            "text": text_list[i]
        })

    driver.quit()
    return result


def search(key):
    start = time.time()
    pool = Pool(5)
    num = [(key,x) for x in range(5)]
    print(num)
    res = pool.map(one_page, num)
    print(res)
    end = time.time()
    print(end-start)
    return res