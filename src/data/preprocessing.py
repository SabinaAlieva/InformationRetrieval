import pandas as pd
import string
import re
import nltk
import collections

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import pymorphy2


stop_words = stopwords.words('russian')
morph = pymorphy2.MorphAnalyzer()

def preprocessing(text):
    # text = str(text)
    text = re.sub(r"^\s+|\n|\r|\t|\s+$", "", text) # отступы
    text = re.sub(r'.[0-9]+', ' ', text) # цифры
    text = re.sub(r'.[a-z]+', ' ', text) # английские символы
    text = re.sub(r'[^\w\s]',' ', text) # пунктуация
    text = text.lower() # регистр
    text = " ".join([word for word in text.split(" ") if (word not in stop_words)]) # стоп-слова
    text = " ".join([t for t in text.split(" ") if len(t) > 0]) # лишние пробелы
    text = " ".join([morph.parse(word)[0].normal_form for word in text.split(" ")]) # лемматизация
    return text


if __name__ == "__main__":
    # df = pd.read_csv("pikabu_dataset.csv")
    df = pd.read_csv("hot_dataset.csv")
    df_text = df[['Title', 'Tags', 'Text']]

    df_text['Text'] = df_text.Text.apply(preprocessing)
    df_text['Tags'] = df_text.Tags.apply(preprocessing)
    df_text['Title'] = df_text.Title.apply(preprocessing)

    df['Text'] = df_text['Text']
    df['Title'] = df_text['Title']
    df['Tags'] = df_text['Tags']

    df.to_csv("hot_dataset_processed.csv")