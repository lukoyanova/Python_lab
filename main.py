import string
import nltk
import re
from nltk.stem.snowball import RussianStemmer

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')

russianStemmer = RussianStemmer(False)

ignore = set(nltk.corpus.stopwords.words('russian'))
stemedIgnore = set()
for word in ignore:
    stemedIgnore.add(russianStemmer.stem(word))
ignore |= stemedIgnore
ignore |= {'', ' ', '»', '«', '--', 'наш'}
for char in string.punctuation:
    ignore.add(char)
regexp = re.compile('[\d|.`—–-…]+')
link_regexp = re.compile('\.com|\.net|\.ru')

if __name__ == '__main__':
    with open('data.txt', encoding='utf8') as file:
        text = file.read()
    words = []
    tokens = nltk.word_tokenize(text)
    for token in [token for token in tokens if token not in ignore
                                               and not regexp.search(token)
                                               and not link_regexp.search(token)]:
        word = russianStemmer.stem(token)
        if word not in ignore:
            words.append(word)

    freq = nltk.FreqDist(words)
    words_count = len(words)
    with open('frequency.txt', 'w', encoding='utf8') as result_file:
        for pair in freq.most_common():
            result_file.write('{} - {} - {:.2%}\n'.format(pair[0], pair[1], pair[1] / words_count))
