import pandas as pd
from sentences.models import Sentence


def add(lang, domain, source=None):
    Sentence.objects.filter(language__exact=lang, category__exact=domain).delete()
    df_chunks = pd.read_csv("./data/" + lang + "/" + domain + "-sentences-scored.tsv", sep="\t", index_col=0, names=["id", "sentence", "sentence_length", "avg_word_length"]).sample(200000)
    for df_chunk in [df_chunks]:
        sentences = []
        for index, row in df_chunk.iterrows():
            sentences.append(Sentence(
                content=row["sentence"],
                sentence_length=row["sentence_length"],
                avg_word_length=row["avg_word_length"],
                source=source,
                language=lang,
                category=domain
            ))
        Sentence.objects.bulk_create(sentences)
