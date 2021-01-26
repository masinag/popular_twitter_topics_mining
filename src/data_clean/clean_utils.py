import regex as re
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import nltk
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

STOP_WORDS = set(stopwords.words('english')).union({"can't", "get", "let", "th", "pm"})
PUNCTUATION = '!"”“#@$€£%&()*+,-./:;<=>?[\\]^_{|}~•…–—'

# ------- REGEX -------

URL_REGEX = re.compile("((http|https)\:\/\/)?[a-z0-9\.\/\?\:@\-_=#]+\.([a-z]){2,6}([a-z0-9\.\&\/\?\:@\-_=#])*")
APOSTROPHE_REGEX = re.compile("[’`]")
NUMBER_REGEX = re.compile("\d+")
TRUNKED_REGEX = re.compile("\w+…")
PUNCTUATION_REGEX = re.compile("["+PUNCTUATION + "]+")
EMOJI_REGEX = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        "]+", flags=re.UNICODE)


REPLACE_RE = [
              (URL_REGEX                         , ' '),
              (TRUNKED_REGEX                     , ''),
              (NUMBER_REGEX                      , ' '),
              (APOSTROPHE_REGEX                  , '\''),
              (PUNCTUATION_REGEX                 , ' '),
              (EMOJI_REGEX                       , ' '),
              (re.compile('(?:new )?coronavirus'), 'covid'),
              (re.compile('sarscov'), 'covid'),
              (re.compile(r'(?:donald)?\btrump'), 'realdonaldtrump')
              ]



def get_wordnet_pos(word):
    """
    Map POS tag to first character lemmatize() accepts
    source: https://www.machinelearningplus.com/nlp/lemmatization-examples-python/ 
    """
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)
