import re
import time
import urllib.request
from urllib.parse import urlparse
import random


class ttl_cached(object):
    def __init__(self, ttl):
        self.cache = {}
        self.ttl = ttl

    def __call__(self, func):
        def wrapped(*args):
            now = time.time()
            if args in self.cache:
                value, last_update = self.cache[args]
                if self.ttl > 0 and now - last_update > self.ttl:
                    value = func(*args)
                    self.cache[args] = (value, now)
                return value
            else:
                value = func(*args)
                self.cache[args] = (value, now)
                return value
        return wrapped


def parse_lib_ru_book(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc != 'lib.ru':
        raise ValueError('book must be from lib.ru')
    elif not parsed_url.path.endswith('.txt'):
        raise ValueError('invalid book url')

    resource = urllib.request.urlopen(url)
    content = resource.read().decode(
        resource.headers.get_content_charset())

    title = re.findall(r'<h2[^>]*>([^<]+)</h2>', content)[0]

    try:
        raw_text = content.split('</ul>', 1)[1].split('<pre>')[0]
        text = re.sub(r'<.*?>', '', raw_text).strip()
    except IndexError:
        text = None
    return title, text


@ttl_cached(3600)
def text_to_sentences(source):
    """Simple text to sentences parser"""
    raw_text = source.replace('--', '\u2014')
    raw_text = raw_text.replace('\n', ' ')
    text_list = list(raw_text)

    raw_text = ''.join(text_list)
    raw_text = re.sub(' +', ' ', raw_text)

    sentences = re.split(r'(?<=[!?.])(?<!\d.)[^\.]', raw_text)
    sentences = list(filter(None, sentences))
    sentences = [s.strip() for s in sentences]

    return sentences


def get_random_sentences(sentences):
    big_sentences = list(filter(lambda x: len(x) > 50, sentences))
    length = len(big_sentences)
    if length >= 5:
        chosen = random.sample(big_sentences, 5)
    else:
        chosen = random.sample(big_sentences, length)
    return chosen
