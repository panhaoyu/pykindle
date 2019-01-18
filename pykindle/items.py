import os
from pykindle import readers


class FieldNotSetError(Exception):
    """
    When user get a field of an item that has not been set yet, raise.
    """

    def __init__(self, field):
        super(FieldNotSetError, self).__init__('{} not set.'.format(field))


class Item(dict):
    """
    Item represents an asset of mobi files.
    This is a base class, you should inherit from it.

    Mobi file consists of several assets and a manifest.
    Each item renders to a asset,
    including articles, images and manifest files.

    Item class inherited from python dict class.
    You can set attributes in two ways:

    >>> item = Item()
    >>> item['href'] = 'path/to/item'
    >>> assert item.href == 'path/to/item'
    >>> item.href = 'path/to/item/changed'
    >>> assert item['href'] = 'path/to/item/changed'

    """

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self._default = dict()

    def __getitem__(self, key):
        assert isinstance(key, str)
        if key in self:
            return super(Item, self).__getitem__(key)
        elif key in self._default:
            return self._default[key]
        else:
            raise FieldNotSetError(key)

    def __setitem__(self, key, value):
        super(Item, self).__setitem__(key, value)

    @property
    def href(self):
        """
        Mobi file is just like a html website,
        and each asset has it's relative url in the mobi file.
        Html assets get other html assets and image assets by relative url.
        """
        return self['href']

    @href.setter
    def href(self, value):
        assert isinstance(value, str)
        self['href'] = value

    @property
    def media_type(self):
        """
        Every mobi asset has a field to indicates what it is, for example,
        application/xhtml+xml represents an article,
        image/jpg represents a photo in jpg format.
        """
        return self['media_type']

    @media_type.setter
    def media_type(self, value):
        assert isinstance(value, str)
        assert '/' in value
        self['media_type'] = value

    @property
    def id(self):
        """
        Id field should be a string! Not integer!
        Just like html elements has a "id" field,
        mobi assets also have such field.
        The difference is that in mobi assets, "id" field in required.
        """
        return self['id']

    @id.setter
    def id(self, value):
        assert isinstance(value, str)
        self['id'] = value

    @property
    def source(self):
        """
        Source is the main content of the asset.
        It will later send to self.reader.render to get the rendered result.
        """
        return self['source']

    @source.setter
    def source(self, value):
        assert value is not None
        self['source'] = value

    @property
    def reader(self):
        """
        Smetimes we need to convert some files to mobi supported assets.
        That's why we use reader.
        Reader should be a instance of pykindle.reader.Reader class.
        Item will call self.reader.render(self.source) to generate rendered assets.
        """
        return self['reader']

    @reader.setter
    def reader(self, value):
        assert isinstance(value, readers.Reader)
        self['reader'] = value

    @property
    def content(self):
        """
        Readonly field.
        It just return the value of self.reader.render(self.source).
        """
        return self.reader.render(self.source)

    def write(self, directory):
        """
        Write the rendered content to a file.
        File path is calculated by os.path.join(directory, self.href).
        """
        path = os.path.join(directory, *self.href.split('/'))
        with open(path, mode='w', encoding='utf-8') as file:
            file.write(self.content)


class ArticleItem(Item):
    """
    ArticleItem represents an real html article.
    This is the main body of your book.

    This class is used for inherit.

    Default attributes:
        title = Untitled
        author = No Author
        description = No description
        category = default
    """

    def __init__(self, *args, **kwargs):
        super(ArticleItem, self).__init__(*args, **kwargs)
        self.media_type = 'application/xhtml+xml'
        self._default.update({
            'title': 'Untitled',
            'author': 'No Author',
            'description': 'No description.',
            'category': 'default',
        })

    @property
    def title(self):
        """
        The title of article.
        """
        return self['title']

    @title.setter
    def title(self, value):
        assert isinstance(value, str)
        self['title'] = value

    @property
    def author(self):
        """
        The author of article.
        """
        return self['author']

    @author.setter
    def author(self, value):
        assert isinstance(value, str)
        self['author'] = value

    @property
    def description(self):
        """
        The description of article.
        """
        return self['description']

    @description.setter
    def description(self, value):
        assert isinstance(value, str)
        self['description'] = value

    @property
    def category(self):
        """
        Optional.
        If you generates a magazine book, this field is used to calculate the magazine category.
        Deprecated. We will create a Category class to do this.
        :return:
        """
        return self['category']

    @category.setter
    def category(self, value):
        assert isinstance(value, str)
        self['category'] = value

    @property
    def content(self):
        return self.reader.render(self.title, self.author, self.description, self.source)


class HtmlArticleItem(ArticleItem):
    """
    HtmlArticleItem represents a html article.
    Although all the articles in mobi files are html,
    we have other ArticleItem like MarkdownArticleItem to convert other formats to html.
    """

    def __init__(self, *args, **kwargs):
        super(HtmlArticleItem, self).__init__(*args, **kwargs)
        self.reader = readers.HtmlReader()


class MarkdownArticleItem(ArticleItem):
    """
    MarkdownArticleItem reads a markdown source.
    """

    def __init__(self, *args, **kwargs):
        super(MarkdownArticleItem, self).__init__(*args, **kwargs)
        self.reader = readers.MarkdownReader()


class ImageItem(Item):
    """
    ImageItem represents a image asset.
    It has a positional argument, image_format='jpeg', alternative formats are jpeg, png, gif
    """
    def __init__(self, image_format='jpeg', *args, **kwargs):
        super(ImageItem, self).__init__(*args, **kwargs)
        assert image_format in ('jpeg', 'png', 'gif')
        self.image_format = image_format
        self.media_type = 'image/' + image_format
        self.reader = readers.ImageReader()


class CoverImageItem(ImageItem):
    """
    CoverImageItem represents a cover image.
    """
    pass


class NcxItem(Item):
    """
    NcxItem is used to generate ncx file.
    Ncx file is the category of a book.
    It will automatically added to the book when book.create is called.
    """
    def __init__(self, *args, **kwargs):
        super(NcxItem, self).__init__(*args, **kwargs)
        self.media_type = 'application/x-dtbncx+xml'
        self._default.update({
            'id': 'ncx',
            'href': 'ncx.toc',
            'title': 'Untitled',
            'author': 'No Author',
        })

    @property
    def title(self):
        return self['title']

    @title.setter
    def title(self, value):
        assert isinstance(value, str)
        self['title'] = value

    @property
    def author(self):
        return self['author']

    @author.setter
    def author(self, value):
        assert isinstance(value, str)
        self['author'] = value


class MagazineNcxItem(NcxItem):
    """
    MagazineNcxItem represents a magazine toc.
    The way to implement magazine is very ugly, and we'll reconstruct these classes.
    """
    def __init__(self, *args, **kwargs):
        super(MagazineNcxItem, self).__init__(*args, **kwargs)
        self.reader = readers.MagazineNcxReader()

    @property
    def categories(self):
        return self['categories']

    @categories.setter
    def categories(self, value):
        assert isinstance(value, list)
        for category, articles in value:
            if not isinstance(category, str):
                raise ValueError('category should be a string.')
            for article in articles:
                if not isinstance(article, ArticleItem):
                    raise ValueError('article should be a pykindle.items.Article object')
        self['categories'] = value

    @property
    def content(self):
        return self.reader.render(title=self.title, author=self.author, categories=self.categories)


__all__ = ['Item', 'ArticleItem', 'HtmlArticleItem', 'MarkdownArticleItem', 'ImageItem', 'CoverImageItem', 'NcxItem',
           'MagazineNcxItem', 'FieldNotSetError']
