import pandas as pd
import html
import csv
import numpy as np
from functools import reduce
from clean_utils import STOP_WORDS, REPLACE_RE, get_wordnet_pos
from collections import Counter
import nltk
from nltk.stem import WordNetLemmatizer 

# TF.IDF(ik) = fik/(max_j fjk) * log2(N/ni)
tf_idfs = []
errors = []
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
    global errors, tf_idfs
    for i, tweet in enumerate(tweets):
        if not tweet:
            continue
        tf = Counter(tweet)
        m = max(tf.values())
        
        curr_tf_idfs = {}
        for term in set(tweet):
            curr_tf_idfs[term] = (tf[term]/m * np.log(N / df[term]))
        tf_idfs.append(curr_tf_idfs)

    return tweets.apply(lambda l : ' '.join(set(l)))

def is_token(term):
    return len(term) > 1 and (term not in STOP_WORDS) and (term not in ["n't"])

def to_lem(term):
    global lemmatizer
    term = term.strip('\'').rstrip("'s")
    if term:
        term = lemmatizer.lemmatize(term, get_wordnet_pos(term))
    return term

def clean_text(tweet):
    tweet = html.unescape(tweet).lower()
    # replace strings such as special characters with blanks as specified in REPLACE_RE
    tweet = reduce(lambda t, rr: rr[0].sub(rr[1], t), REPLACE_RE, tweet)
    return list(filter(is_token, map(to_lem, nltk.word_tokenize(tweet))))

def clean_dataset(dataset, output):
    data = pd.read_csv(dataset, usecols=('date', 'text'), encoding='utf-8').sort_values(by = 'date')
    data['clean_text'] = data.text.apply(clean_text)
    data['tokens'] = tokenize(data.clean_text)
    # print("Errors:")
    # global errors
    # print(data.text[errors])
    # print(f"TFIDF\nmax:{np.max(tf_idfs)}\nmin:{np.min(tf_idfs)}\navg:{np.mean(tf_idfs)}")
    with open("../../data/tmp_tf_idfs.dict", "w+") as f:
        f.write(str(tf_idfs))
        f.write("\n")
    data.to_csv(output, index=False, columns=('date', 'tokens'), header=('time', 'tokens'), encoding='utf-8', quoting = csv.QUOTE_MINIMAL)

if __name__ == '__main__':
    dataset = '../../data/original_covid19_tweets.csv'
    output = '../../data/cleaned_covid19_tweets.csv'
    clean_dataset(dataset, output)
