import os
from pykindle import readers


class Item(object):
    href: str = None
    media_type: str = None
    id = None
    source = None
    reader: readers.Reader = None

    def verify(self):
        assert isinstance(self.href, str)
        assert isinstance(self.media_type, str)
        assert '/' in self.media_type
        assert isinstance(self.id, int)
        assert not (self.source is None)
        assert isinstance(self.reader, readers.Reader)
        return True

    @property
    def content(self):
        return self.reader.render(self.source)

    def write(self, directory):
        path = os.path.join(directory, *self.href.split('/'))
        with open(path, mode='w', encoding='utf-8') as file:
            file.write(self.content)


class ArticleItem(Item):
    def __init__(self):
        self.media_type = 'application/xhtml+xml'
        self.title = 'Untitled'
        self.author = 'Notset'
        self.description = 'No description.'
        self.category = 'default'

    def verify(self):
        super(ArticleItem, self).verify()
        assert isinstance(self.title, str)
        assert isinstance(self.author, str)
        assert isinstance(self.description, str)

    @property
    def content(self):
        return self.reader.render(self.title, self.author, self.description, self.source)


class HtmlArticleItem(ArticleItem):
    def __init__(self):
        super(HtmlArticleItem, self).__init__()
        self.reader = readers.HtmlReader()


class MarkdownArticleItem(ArticleItem):
    def __init__(self):
        super(MarkdownArticleItem, self).__init__()
        self.reader = readers.MarkdownReader()


class ImageItem(Item):
    def __init__(self, image_format='jpeg'):
        assert image_format in ('jpeg', 'png', 'gif')
        self.image_format = image_format
        self.media_type = 'image/' + image_format
        self.reader = readers.ImageReader()


class CoverImageItem(ImageItem):
    pass


class NcxItem(Item):
    def __init__(self):
        self.media_type = 'application/x-dtbncx+xml'
        self.title = 'Untitled'
        self.author = 'default'
        self.href = 'ncx.toc'
        self.id = 'ncx'


class MagazineNcxItem(NcxItem):
    def __init__(self):
        super(MagazineNcxItem, self).__init__()
        self.categories = None
        self.reader = readers.MagazineNcxReader()

    @property
    def content(self):
        return self.reader.render(title=self.title, author=self.author, categories=self.categories)
