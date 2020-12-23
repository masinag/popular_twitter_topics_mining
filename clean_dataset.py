import pandas as pd
import csv
import regex as re
import html
# import nltk
from memory_profiler import profile
from utils import DATES, STOP_WORDS
# stop_words = set(nltk.corpus.stopwords.words('english'))
# word_rooter = nltk.stem.snowball.PorterStemmer(ignore_stopwords=False).stem

my_punctuation = '!"”“$€£%&\'()*+,-./:;<=>?[\\]^_`{|}~•…–'
# email_regex = re.compile("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
# user_regex = re.compile("@[A-Za-z]+[A-Za-z0-9-_]+")
url_regex = re.compile("((http|https)\:\/\/)?[a-z0-9\.\/\?\:@\-_=#]+\.([a-z]){2,6}([a-z0-9\.\&\/\?\:@\-_=#])*")
punctuation_regex = re.compile("["+my_punctuation + "]+")
emoji_regex = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
                           "]+", flags = re.UNICODE)

# def remove_emails(tweet):
#     return email_regex.sub("", tweet)
# def remove_users(tweet):
#     return user_regex.sub("", tweet)

def clean_tweet(tweet, bigrams=False):
    tweet = html.unescape(tweet)
    tweet = url_regex.sub(" ", tweet.lower()) # remove links
    # tweet = number_regex.sub("", tweet) # remove numbers
    tweet = emoji_regex.sub(" ", tweet) # remove emoji
    tweet = punctuation_regex.sub(" ", tweet) # strip punctuation
    return " ".join((filter(lambda x : len(x) > 1 and x not in STOP_WORDS, tweet.split())))

# @profile
def clean_dataset(dataset, output):
    data = pd.read_csv(dataset, usecols=("date", "text"), encoding="utf-8").sort_values(by = "date")
    data['tokens'] = data.text.apply(clean_tweet)
    data.to_csv(output, index=False, columns=("date", "tokens"), encoding="utf-8", quoting=csv.QUOTE_NONNUMERIC)

    # with open(dataset) as fi, open(output, "w", newline="") as fo:
    #     reader = csv.reader(fi)
    #     writer = csv.writer(fo)
    #     header = {)e : i for i, e in enumerate(next(reader))}
    #     writer.writerow(["date", "text", "tokens"])
    #     for r in reader:
    #         tokens = clean_tweet(r[header["text"]])
    #         writer.writerow([r[header["date"]], r[header["text"]], tokens])
        

if __name__ == "__main__":
    dataset = "data/covid19_tweets.csv"
    output = "data/tweets_clean.csv"
    clean_dataset(dataset, output)

