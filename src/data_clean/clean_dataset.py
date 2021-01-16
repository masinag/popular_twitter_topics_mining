import pandas as pd
import html
import csv
from functools import reduce
from clean_utils import STOP_WORDS, REPLACE_RE


def clean_tweet(tweet, bigrams=False):
    tweet = html.unescape(tweet).lower()
    # replace strings such as special characters with blanks as specified in REPLACE_RE
    tweet = reduce(lambda t, rr: reduce(lambda v, r: r.sub(rr[0], v), rr[1], t), REPLACE_RE, tweet)
    return ' '.join(set(filter(lambda x : len(x) > 1 and x not in STOP_WORDS, tweet.split())))

def clean_dataset(dataset, output):
    data = pd.read_csv(dataset, usecols=('date', 'text'), encoding='utf-8').sort_values(by = 'date')
    data['tokens'] = data.text.apply(clean_tweet)
    data.to_csv(output, index=False, columns=('date','tokens'), header=('time', 'tokens'), encoding='utf-8', quoting = csv.QUOTE_MINIMAL)

if __name__ == '__main__':
    dataset = '../../data/original_covid19_tweets.csv'
    output = '../../data/cleaned_covid19_tweets.csv'
    clean_dataset(dataset, output)

