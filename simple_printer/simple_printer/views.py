from django.shortcuts import render
from .utils import *


def all(request):
    title, text = parse_lib_ru_book('http://lib.ru/FOUNDATION/r_pervyj_zakon.txt')
    sentences = text_to_sentences(text)
    chosen = get_random_sentences(sentences)

    return render(request, 'index.html',
                  {
                      'title': title,
                      'sentences': chosen,
                  })
