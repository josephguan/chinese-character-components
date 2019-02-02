from typing import List, Dict

from lxml import html

from spider.downloader import HtmlDownloader


class Word(object):
    def __init__(self, number: int, word: str):
        self.id = number
        self.word = word

    def __str__(self):
        template = 'Word({number},{word})'
        return template.format(number=self.id, word=self.word)


class WikiSpider(object):

    @staticmethod
    def wiki_url() -> str:
        return "https://zh.wikisource.org/zh-hans/%E9%80%9A%E7%94%A8%E8%A7%84%E8%8C%83%E6%B1%89%E5%AD%97%E8%A1%A8#%E9%99%84%E4%BB%B62._%E3%80%8A%E9%80%9A%E7%94%A8%E8%A7%84%E8%8C%83%E6%B1%89%E5%AD%97%E8%A1%A8%E3%80%8B%E7%AC%94%E7%94%BB%E6%A3%80%E5%AD%97%E8%A1%A8"

    @staticmethod
    def parse(page: str, id_list: List[int]) -> Dict[int, str]:
        tree = html.fromstring(page)
        words: List[str] = tree.xpath('//*[@id="mw-content-text"]/div/table/tbody/tr/td/dl/dd/text()')
        result: Dict[int, str] = {}
        for w in words:
            ls = w.split(' ')
            num = int(ls[0])
            word = ls[1]
            if word != "" and num in id_list:
                result[num] = word
        return result

    def crawl(self, id_list: List[int]) -> Dict[int, str]:
        """get level 1 characters, range from 1 to 3500"""
        page = HtmlDownloader.download(self.wiki_url())
        return self.parse(page, id_list)


if __name__ == '__main__':
    wiki = WikiSpider()
    for k, v in wiki.crawl(list(range(1, 5))).items():
        print(k, v)
