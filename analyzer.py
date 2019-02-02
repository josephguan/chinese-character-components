from typing import List, Tuple

import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

RADICAL_NAME_FILE = r'./data/radical_names.csv'
FONT = r'./resources/SIMYOU.TTF'
BACKGROUND = r'./resources/star.jpg'


class Analyzer(object):

    def __init__(self, files: List[str]):
        self.files = files

    @staticmethod
    def read_csv(files) -> pd.DataFrame:
        df = pd.DataFrame()
        for f in files:
            df = df.append(pd.read_csv(f, header=None, names=["id", "word", "radical", "tones"]))
        return df

    def stat_radical(self) -> pd.DataFrame:
        word_df = self.read_csv(self.files)
        name_df = pd.read_csv(RADICAL_NAME_FILE)
        join_df = pd.merge(word_df, name_df, how='left', on=['radical'])
        grouped_df = join_df.groupby("name").agg({'word': 'count', 'radical': lambda x: ','.join(set(x))})
        sorted_df = grouped_df.reset_index().rename(columns={'word': 'count'}).sort_values(['count'], ascending=False)
        # return join_df.groupby("name")['word'].count().reset_index(name='count').sort_values(['count'], ascending=False)
        return sorted_df

    def show_word_cloud(self):
        wc = self.get_word_cloud()
        plt.imshow(wc)
        plt.axis("off")
        plt.show()

    def get_word_cloud(self) -> WordCloud:
        df = self.stat_radical()
        freq = {}
        for a, b in df[['name', 'count']].values:
            freq[a] = b
        # bg_pic = plt.imread(BACKGROUND)
        # wc = WordCloud(font_path=FONT, mask=bg_pic, width=800, height=600)
        wc = WordCloud(font_path=FONT, width=400, height=200, background_color='white')
        wc.generate_from_frequencies(frequencies=freq)
        return wc

    def get_topN(self, n: int) -> Tuple[pd.DataFrame, float]:
        df = self.stat_radical()
        top_df = df[df['name'].isin(['点', '一', '竖', '撇']) == False].head(n)
        top_count = top_df['count'].sum()
        total_count = df['count'].sum()
        ratio = top_count / total_count
        return top_df, ratio

    def write_word_could(self, filename: str):
        wc = self.get_word_cloud()
        wc.to_file(filename)

    def write_topN(self, filename: str, n: int):
        data, rate = self.get_topN(n)
        print('coverage ratio：%.2f%%' % (rate * 100))
        data.to_csv(filename, index=False, sep='|')


if __name__ == '__main__':
    analyzer = Analyzer(['./data/level1.csv', './data/level2.csv'])
    analyzer.write_word_could('./output/wordcloud.jpg')
    analyzer.write_topN('./output/top40.csv', 40)
    analyzer.write_topN('./output/top20.csv', 20)