from django.db import connection
from .nlp import sen_features
import random


def escape(content):
    return content.replace("'", "''")


def build_difficulty_sql(difficulty, lang):
    lang_features = sen_features[lang]
    lang_sen_features = lang_features["sentence_length"]
    if difficulty is None:
        return "True"
    if difficulty == 0:
        return f"sentence_length <= {lang_sen_features[0]} AND avg_word_length <= {lang_features['word_length_thresh']}"
    elif difficulty == 1:
        return f"sentence_length <= {lang_sen_features[1]} AND sentence_length > {lang_sen_features[0]}"
    return f"sentence_length > {lang_sen_features[2]}"


def query_sentences(word_forms, difficulty, categories, lang):
    cursor = connection.cursor()
    temp_tblname = f"word_forms_{random.randint(10000000,99999999)}"

    word_forms_sql = ", ".join(["(%s)" for _ in word_forms])
    categories_sql = "(" + ", ".join(["%s" for _ in categories]) + ")"
    difficulty_sql = build_difficulty_sql(difficulty, lang)

    cursor.execute(f"CREATE TEMPORARY TABLE {temp_tblname} (word VARCHAR(256))")
    cursor.execute(f"INSERT INTO {temp_tblname} (word) VALUES {word_forms_sql}", [escape(w) for w in word_forms])
    cursor.execute(f"""
        SELECT * FROM (
            SELECT 
                sen.ref_id, 
                sen.content, 
                sen.source, 
                sen.category, 
                {temp_tblname}.word AS word, 
                ROW_NUMBER() OVER (PARTITION BY word ORDER BY id ASC) AS rn 
            FROM (
                SELECT * FROM sentences_sentence 
                WHERE language=%s AND category IN {categories_sql} AND {difficulty_sql}) sen 
                    INNER JOIN {temp_tblname} 
                    ON sen.content LIKE '%% ' || word || ' %%' 
                    OR sen.content LIKE '%% ' || word || '.%%' OR sen.content LIKE '%% ' || word || ',%%' 
                    OR sen.content LIKE '%% ' || word || '!%%' OR sen.content LIKE '%% ' || word || '?%%' 
                    OR sen.content LIKE '%% ' || word || ':%%' OR sen.content LIKE '%% ' || word || ';%%') 
            sub WHERE sub.rn <= 10""", [lang] + categories)
    res = cursor.fetchall()
    cursor.close()
    return res
