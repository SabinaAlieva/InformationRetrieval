import pandas as pd
import string
import re
import nltk
import collections

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import pymorphy2

from pyspark import SparkContext
from pyspark.sql import SparkSession

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

filename_source = "datapikabu_dataset_new.csv"
filename = "pikabu_dataset_longText.csv"
filename_new = "pikabu_dataset_clear.csv"
filename_good = "pikabu_dataset_good.csv"

if __name__ == "__main__":

    df = pd.read_csv(filename_source)
    df_enough = df[df['Text'].map(lambda x: len(str(x)) > 1000)]
    df_enough.to_csv(filename, index=False)

    sc = SparkContext(master='local[*]')

    spark = SparkSession \
        .builder \
        .appName("PySpark") \
        .getOrCreate()

    df_spark = spark.read.csv(filename, inferSchema=True, header=True) \
        .toDF('Number', 'FileName', 'Title', 'Link', 'ArticleId', 'Date', 'Views', \
               'Author', 'Tags', 'AmountComments', 'Rating', 'Text')

    prepr = F.udf(preprocessing, StringType())

    df_clear = df_spark.withColumn('Text', prepr(df_spark['Text'])) \
        .withColumn('Tags', prepr(df_spark['Tags'])) \
        .withColumn('Title', prepr(df_spark['Title']))

    df_clear = df_clear.toPandas()
    df_clear.to_csv(filename_new)

    df = df_clear[['Title', 'Link', 'Date', 'Views', 'Author', 'Tags', 'AmountComments', 'Rating', 'Text']]
    df.to_csv(filename_good, index = None)