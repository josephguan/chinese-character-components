import logging
from typing import List, Tuple
from urllib.parse import quote

from lxml import html

from spider import ChineseChar
from spider.downloader import HtmlDownloader


class BaiduSpider(object):

    @staticmethod
    def baidu_hanyu_url(word: str) -> str:
        return "https://hanyu.baidu.com/s?wd={word}&ptype=zici".format(word=quote(word))

    @staticmethod
    def parse(page: str) -> Tuple[List[str], List[str]]:
        tree = html.fromstring(page)
        tone = tree.xpath('//*[@id="pinyin"]/span/b/text()')
        radical = tree.xpath('//*[@id="radical"]/span/text()')
        return tone, radical

    def query(self, word: str) -> ChineseChar:
        page = HtmlDownloader.download(self.baidu_hanyu_url(word))
        if page != "":
            tone, radical = self.parse(page)
            if len(radical) == 0:
                return ChineseChar(word, " ", tone)
            else:
                return ChineseChar(word, radical[0], tone)
        else:
            logging.error("parse {w} failed!".format(w=word))
            raise Exception("parse {w} failed!".format(w=word))


if __name__ == '__main__':
    words = ['床', '前', '明', '月', '光']
    baidu = BaiduSpider()
    for w in words:
        print(baidu.query(w))
