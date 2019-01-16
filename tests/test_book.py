import os
import pykindle

DATA = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')


def test_book():
    magazine = pykindle.NormalBook()
    with open(os.path.join(DATA, '1.md'), mode='r', encoding='utf-8') as file:
        content = file.read()
    item = pykindle.MarkdownArticleItem()
    item.source = content
    item.href = '1.html'
    magazine.append(item)
    print(len(magazine.create()) / 8 / 1024)


test_book()
