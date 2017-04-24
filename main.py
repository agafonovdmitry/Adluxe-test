import re
import sys
import time
import argparse
import urllib.request
from urllib.parse import urlparse


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


@ttl_cached(3600)
def parse_lib_ru_book(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc != 'lib.ru':
        raise ValueError('book must be from lib.ru')
    elif not parsed_url.path.endswith('.txt'):
        raise ValueError('invalid book url')

    resource = urllib.request.urlopen(url)
    print("*** Quering LIB.ru!")
    content = resource.read().decode(
        resource.headers.get_content_charset())

    title = re.findall(r'<h2[^>]*>([^<]+)</h2>', content)[0]

    try:
        raw_text = content.split('</ul>', 1)[1].split('<pre>')[0]
        text = re.sub(r'<.*?>', '', raw_text).strip()
    except IndexError:
        text = None
    return title, text


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lib.ru book parser')
    parser.add_argument('--url', action='store',
                        help='book URL from lib.ru', required=True)
    args = parser.parse_args()
    result = parse_lib_ru_book(args.url)
    print(result[0], file=sys.stderr)
    print(result[1])

