import pandas as pd
import html
import csv
import numpy as np
from functools import reduce
from clean_utils import STOP_WORDS, REPLACE_RE, get_wordnet_pos
from collections import Counter
import nltk
from nltk.stem import WordNetLemmatizer
import time
from argparse import ArgumentParser
from matplotlib import pyplot as plt

LEMMATIZE = True

TF_IDF_THRESHOLD = 3.20

tf_idfs = []
lemmatizer = WordNetLemmatizer()

def get_df(tweets):
    df = {}
    for tweet in tweets:
        for term in set(tweet):
            df[term] = df.get(term, 0) + 1
    return df

def tokenize(tweets):
    df = get_df(tweets)
    N = tweets.shape[0]
    print(tweets[0], set(tweets[0]))
    # global tf_idfs
    rt_tweets = []
    for i, tweet in enumerate(tweets):
        if not tweet:
            continue
        tf = Counter(tweet)
        m = max(tf.values())
        rt = []
        for term in set(tweet):
            tf_idf = (tf[term]/m * np.log(N / df[term]))
            tf_idfs.append(tf_idf)
            if tf_idf >= TF_IDF_THRESHOLD:
                rt.append(term)
        
        rt_tweets.append(rt)

    return pd.Series(rt_tweets).apply(lambda l : ' '.join(l))

def is_token(term):
    return len(term) > 1 and (term not in STOP_WORDS) and (term not in ["n't"])

def to_lem(term):
    global lemmatizer
    term = term.strip('\'').rstrip("'s")
    if LEMMATIZE and term:
        term = lemmatizer.lemmatize(term, get_wordnet_pos(term))
    return term

def clean_text(tweet):
    tweet = html.unescape(tweet).lower()
    # replace strings such as special characters with blanks as specified in REPLACE_RE
    tweet = reduce(lambda t, rr: rr[0].sub(rr[1], t), REPLACE_RE, tweet)
    return ' '.join(filter(is_token, map(to_lem, nltk.word_tokenize(tweet))))

def clean_dataset(dataset, output):
    data = pd.read_csv(dataset, usecols=('date', 'text'), \
        encoding='utf-8').sort_values(by = 'date')
    data['clean_text'] = data.text.apply(clean_text)

    data.to_csv(output, index=False, columns=('date', 'clean_text'), \
        encoding='utf-8', quoting = csv.QUOTE_MINIMAL)

def tokenize_dataset(dataset, output):
    data = pd.read_csv(dataset, usecols=('date', 'clean_text'), \
        encoding='utf-8', converters={'clean_text' : lambda x : x.split()})
    data['tokens'] = tokenize(data.clean_text)
    tf_idfs.sort(reverse=True)
    
    print(f"""Quantiles:
    0.00 : {np.quantile(tf_idfs, 0.00):.02f}
    0.05 : {np.quantile(tf_idfs, 0.05):.02f}
    0.10 : {np.quantile(tf_idfs, 0.10):.02f}
    0.15 : {np.quantile(tf_idfs, 0.15):.02f}
    0.20 : {np.quantile(tf_idfs, 0.20):.02f}
    0.25 : {np.quantile(tf_idfs, 0.25):.02f}
    0.50 : {np.quantile(tf_idfs, 0.50):.02f}
    0.75 : {np.quantile(tf_idfs, 0.75):.02f}
    1.00 : {np.quantile(tf_idfs, 1.00):.02f}
    """)
    plt.plot(range(len(tf_idfs)), tf_idfs)
    plt.show()
    data.to_csv(output, index=False, columns=('date', 'tokens'), \
        header = ('time', 'tokens'), encoding='utf-8', quoting = csv.QUOTE_MINIMAL)


if __name__ == '__main__':
    start = time.time()
    ap = ArgumentParser()
    ap.add_argument("action", choices=['clean', 'tokenize', 'all'], default='all')

    action = ap.parse_args().action

    if action in ['clean', 'all']:
        dataset = '../../data/original_covid19_tweets.csv'
        output = '../../data/partial_cleaned_covid19_tweets.csv'
        clean_dataset(dataset, output)
    if action in ['tokenize', 'all']:
        dataset = '../../data/partial_cleaned_covid19_tweets.csv'
        output = '../../data/cleaned_covid19_tweets.csv'
        tokenize_dataset(dataset, output)
    # clean_dataset(dataset, output)
    end = time.time()

    print(f"{end-start:.02f} seconds")

