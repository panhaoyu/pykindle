from pykindle import readers
from pykindle import items


def test_html_render():
    reader = readers.HtmlReader()
    assert reader.render(title='title', author='author', description='description', content='content')


def test_markdown_render():
    reader = readers.MarkdownReader()
    assert reader.render(title='title', author='author', description='description', content='content')


def test_magazine_ncx_render():
    reader = readers.MagazineNcxReader()
    try:
        reader.render(categories=[], title='title', author='author')
        raise AssertionError
    except ValueError:
        pass
    articles = [items.ArticleItem() for i in range(10)]
    for index, article in enumerate(articles):
        article.href = '{}.html'.format(index)
        article.id = str(index)
    assert reader.render(categories=[
        ('category1', articles[:5]),
        ('category2', articles[5:]),
    ], title='title', author='author')
