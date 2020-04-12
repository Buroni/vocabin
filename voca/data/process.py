import numpy as np
import pandas as pd
import sys
import tqdm
import re

lang = sys.argv[1]
domain = sys.argv[2]


def build_base_url(language, domain):
    return "./" + language + "/" + domain


class Sentences:
    def __init__(self, df_sentences):
        self.df_sentences = df_sentences
        self.df_sentences = self.df_sentences.assign(sentence_length=0, avg_word_length=0)
        self.df_sentences = self.df_sentences[(self.df_sentences["sentence"].str.count(r"\.+") <= 1)]
        self.sentences = self.df_sentences[self.df_sentences.columns[0]]

    def score_sentences(self):
        for index, row in tqdm.tqdm(self.df_sentences.iterrows()):
            words = re.findall(r'\w+', row["sentence"])
            self.df_sentences.loc[index, "sentence_length"] = len(words)
            self.df_sentences.loc[index, "avg_word_length"] = np.mean([float(len(w)) for w in words])

    def create_file(self):
        self.score_sentences()
        self.df_sentences.to_csv(f"./{lang}/{domain}-sentences-scored.tsv", sep="\t", mode="a", header=None)


base_url = build_base_url(lang, domain)
df_chunks = pd.read_csv(base_url + "-sentences.tsv", sep="\t", index_col=0, names=["id", "sentence"], chunksize=10000)

for df_chunk in df_chunks:
    s = Sentences(df_chunk)
    s.create_file()
