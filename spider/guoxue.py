import logging
from itertools import chain
from typing import List, Tuple
from urllib.parse import quote

from lxml import html

from spider import ChineseChar
from spider.downloader import HtmlDownloader


class GuoxueSpider(object):

    @staticmethod
    def query_url(word: str) -> str:
        return "http://www.guoxuedashi.com/so.php?sokeytm={word}&ka=100&submit=".format(word=quote(word))

    @staticmethod
    def redirect_url(location: str) -> str:
        location_str = str(location)
        start = location_str.find("'")
        end = location_str.find("'", start + 1)
        href = location_str[start + 1: end]
        url = "http://www.guoxuedashi.com" + href
        return url

    @staticmethod
    def parse(page: str) -> Tuple[List[str], List[str]]:
        tree = html.fromstring(page)
        tone_items = tree.xpath(r'//*[contains(@class, "zui")]//td[2]/table/tr[1]/td/text()')
        radical_items = tree.xpath(r'//*[contains(@class, "zui")]//td[2]/table/tr[2]/td/text()')
        tone_list = [x.replace('拼音：', '') for x in tone_items]
        tone_lists = [x.split(",") for x in tone_list]
        tone = list(chain(*tone_lists))
        radical = [x.replace('部首：', '') for x in radical_items]
        return tone, radical

    def query(self, word: str) -> ChineseChar:
        location = HtmlDownloader.download(self.query_url(word))
        page = HtmlDownloader.download(self.redirect_url(location))
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
    words = ['𤫉', '㸌', '𨭉', '𨟠', '差']
    guoxue = GuoxueSpider()
    for w in words:
        print(guoxue.query(w))
