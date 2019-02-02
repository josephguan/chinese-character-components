# -*- coding: utf-8 -*-

import csv
import logging
import os
import random
import time
from typing import Dict

from spider import ChineseChar
from spider.baidu import BaiduSpider
from spider.guoxue import GuoxueSpider
from spider.wiki import WikiSpider


class Collector(object):

    def __init__(self):
        self.baidu = BaiduSpider()
        self.guoxue = GuoxueSpider()

    @staticmethod
    def get_start_and_end(filename: str):
        min_index = 0
        max_index = 0
        if not os.path.exists(filename):
            return min_index, max_index

        with open(filename, 'r', encoding='UTF-8') as fd:
            reader = csv.reader(fd)
            for line in reader:
                try:
                    number = int(line[0])
                except Exception:
                    continue
                if min_index > number or min_index == 0:
                    min_index = number
                if max_index < number:
                    max_index = number
        return min_index, max_index

    def collect_to_file(self, start: int, end: int, filename: str):
        # get ids to be crawled.
        min_index, max_index = self.get_start_and_end(filename)
        id_list = set(range(start, end + 1)) - set(range(min_index, max_index + 1))
        if len(id_list) == 0:
            logging.info(
                "all items between from {a} to {b} has been downloaded in file {f}".format(a=start, b=end, f=filename))
            return
        logging.info(id_list)

        # crawl character list
        wiki = WikiSpider()
        success = False
        candidates: Dict[int, str] = {}
        while not success:
            try:
                candidates = wiki.crawl(id_list)
                success = True
            except Exception:
                logging.error("open wiki failed...try again.")
                time.sleep(random.randint(0, 3))
        logging.info(candidates)

        # crawl data into file
        with open(filename, 'a', encoding='UTF-8', newline='') as fd:
            writer = csv.writer(fd)
            while len(candidates) > 0:
                (k, v) = candidates.popitem()
                try:
                    time.sleep(random.randint(0, 3))
                    res = self.query(v)
                    print(k, res.word, res.radical, '|'.join(res.tone))
                    writer.writerow([k, res.word, res.radical, '|'.join(res.tone)])
                    fd.flush()
                except Exception as e:
                    candidates[k] = v
                    logging.error("put {v} to candidates again.".format(v=v))

    def query(self, word) -> ChineseChar:
        res = self.guoxue.query(word)
        if res.radical == " ":
            logging.info("can not find {w}, try hanyu.baidu".format(w=word))
            res = self.baidu.query(word)
        return res


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    Collector().collect_to_file(1, 3500, './data/level1.csv')
    Collector().collect_to_file(3501, 6500, './data/level2.csv')
    Collector().collect_to_file(6501, 8102, './data/level3.csv')
