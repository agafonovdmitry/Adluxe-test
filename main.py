import re
import time
import threading
import argparse
import urllib.request
from urllib.parse import urlparse


class LibRuParser:
    def __init__(self):
        self.parsed_book = None

    @staticmethod
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

    def run_parse(self, url, timeout=3600):
        while True:
            self.parsed_book = self.parse_lib_ru_book(url)
            print(self.parsed_book)
            time.sleep(timeout)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lib.ru book parser')
    parser.add_argument('--url', action='store',
                        help='book URL from lib.ru', required=True)
    args = parser.parse_args()

    p = LibRuParser()

    thread = threading.Thread(target=p.run_parse, args=(args.url,))
    thread.start()
