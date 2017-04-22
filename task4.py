import re
from main import parse_lib_ru_book


def text_to_sentences(source):
    """Simple text to sentences parser"""
    raw_text = source.replace('--', '\u2014')

    text_list = list(raw_text)

    for match in re.finditer('\n', raw_text):
        index = match.start()
        if raw_text[index-1] in '.?!-':
            text_list[index] = ''
        else:
            text_list[index] = ' '

    raw_text = ''.join(text_list)
    raw_text = re.sub(' +', ' ', raw_text)

    sentences = re.split(r'(?<=[!?.])(?<!\d.)[^\.]', raw_text)
    sentences = list(filter(None, sentences))
    sentences = [s.strip() for s in sentences]

    return sentences


if __name__ == '__main__':
    title, text = parse_lib_ru_book(
        'http://lib.ru/FOUNDATION/r_pervyj_zakon.txt')
    print(title, '\n')
    for sentence in text_to_sentences(text):
        print(sentence)