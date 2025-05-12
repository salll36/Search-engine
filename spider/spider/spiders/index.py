import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class IndexSpider(CrawlSpider):
    name = "index"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://cn.bing.com/search?q=%E9%98%BF%E8%90%A8%E5%BE%B7"]

    # 链接提取器
    link=LinkExtractor(allow=r"https://cn.bing.com/search?q=%E9%98%BF%E8%90%A8%E5%BE%B7&first=\d+")
    # 规则解析器
    rules = (
        Rule(link, callback="parse_item", follow=True),
    )
    # 页数链接
    def parse_item(self, response):
        print(response)