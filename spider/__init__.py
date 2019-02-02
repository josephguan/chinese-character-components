from typing import List


class ChineseChar(object):
    def __init__(self, word: str, radical: str, tone: List[str]):
        self.word = word
        self.radical = radical
        self.tone = tone

    def __str__(self):
        template = 'ChineseChar({word},{radical},{tone})'
        return template.format(word=self.word, radical=self.radical, tone='|'.join(self.tone))
