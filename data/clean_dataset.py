import pandas as pd
import csv
import regex as re
import html
from functools import reduce
# import nltk
# from memory_profiler import profile
from clean_utils import STOP_WORDS, REPLACE_RE
# stop_words = set(nltk.corpus.stopwords.words('english'))
# word_rooter = nltk.stem.snowball.PorterStemmer(ignore_stopwords=False).stem


# def remove_emails(tweet):
#     return email_regex.sub('', tweet)
# def remove_users(tweet):
#     return user_regex.sub('', tweet)

def clean_tweet(tweet, bigrams=False):
    tweet = html.unescape(tweet).lower()
    # replace strings such as special characters with blanks as specified in REPLACE_RE
    tweet = reduce(lambda t, rr: reduce(lambda v, r: r.sub(rr[0], v), rr[1], t), REPLACE_RE, tweet)

    # tweet = url_regex.sub(' ', tweet.lower()) # remove links
    # tweet = number_regex.sub(' ', tweet) #remove numbers
    # # tweet = number_regex.sub('', tweet) # remove numbers
    # tweet = emoji_regex.sub(' ', tweet) # remove emoji
    # tweet = trunked_regex.sub(' ', tweet) #remove last trunked word
    # tweet = punctuation_regex.sub(' ', tweet) # strip punctuation
    # for word, equivalents in EQUIVALENTS_RE.items():
    #     for re_eq in equivalents:
    #         tweet = re_eq.sub(word, tweet)
    return ' '.join(set(filter(lambda x : len(x) > 1 and x not in STOP_WORDS, tweet.split())))

# @profile
def clean_dataset(dataset, output):
    data = pd.read_csv(dataset, usecols=('date', 'text'), encoding='utf-8').sort_values(by = 'date')
    data['tokens'] = data.text.apply(clean_tweet)
    data.to_csv(output, index=False, columns=('date','tokens'), header=('time', 'tokens'), encoding='utf-8', quoting = csv.QUOTE_MINIMAL)

    # with open(dataset) as fi, open(output, 'w', newline='') as fo:
    #     reader = csv.reader(fi)
    #     writer = csv.writer(fo)
    #     header = {)e : i for i, e in enumerate(next(reader))}
    #     writer.writerow(['date', 'text', 'tokens'])
    #     for r in reader:
    #         tokens = clean_tweet(r[header['text']])
    #         writer.writerow([r[header['date']], r[header['text']], tokens])
        

if __name__ == '__main__':
    dataset = 'original_covid19_tweets.csv'
    output = 'cleaned_covid19_tweets.csv'
    clean_dataset(dataset, output)

