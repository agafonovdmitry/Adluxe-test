import re
import sys
import argparse
import urllib.request
from urllib.parse import urlparse


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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lib.ru book parser')
    parser.add_argument('--url', action='store',
                        help='book URL from lib.ru', required=True)
    args = parser.parse_args()
    result = parse_lib_ru_book(args.url)
    print(result[0], file=sys.stderr)
    print(result[1])
