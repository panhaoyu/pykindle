import os
import markdown
import jinja2

_template_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')


class Reader(object):
    """
    This class is only for inherit.
    Reader is in fact a package of the render function of jinja.
    It renders some args to a mobi asset.
    Renders are only used in items, items will call item.reader.render when generate a book.
    """

    def render(self, *args, **kwargs):
        """
        Render some source to mobi asset.
        """
        pass


class TemplateReader(Reader):
    """
    This class is only used for inherit.
    It defines the jinja2 environment.
    """

    def __init__(self, jinja2_loader=jinja2.FileSystemLoader(_template_dir)):
        self._jinja2 = jinja2.Environment(loader=jinja2_loader)


class HtmlReader(TemplateReader):
    """
    This class renders html source code.
    """

    def render(self, title, author, description, content):
        """
        Title, author, description and content, as their names indicate, are the metadata of the html article.
        """
        super(HtmlReader, self).render()
        template = self._jinja2.get_template('article.html')
        return template.render({
            'title': title,
            'author': author,
            'description': description,
            'content': content,
        })


class MarkdownReader(HtmlReader):
    """
    This class renders markdown source code to mobi asset.
    """

    def __init__(self, markdown_options=None, **kwargs):
        """
        TODO: write a testcase for markdown_options
        """
        super(MarkdownReader, self).__init__(**kwargs)
        self._markdown_options = markdown_options if markdown_options else dict()

    def render(self, title, author, description, content):
        """
        Title, author, description and content, as their names indicate, are the metadata of the html article.
        """
        content = markdown.markdown(content, **self._markdown_options)
        return super(MarkdownReader, self).render(title, author, description, content)


class ImageReader(Reader):
    """
    Used to render image.
    Currently, it just return the source itself.
    """
    def render(self, content):
        return content


class NcxReader(TemplateReader):
    """
    TODO: implement.
    """
    pass


class MagazineNcxReader(NcxReader):
    """
    Render the ncx asset.
    """
    def render(self, categories, title, author):
        """
        It's not stable currently.
        TODO: change the categories behavior.
        """
        assert isinstance(categories, list)
        if len(categories) == 0:
            raise ValueError('There is no category.')
        for category, articles in categories:
            if len(articles) == 0:
                raise ValueError('There is no article in {}'.format(category))
        template = self._jinja2.get_template('magazine.ncx')
        result = template.render({
            'categories': categories,
            'title': title,
            'author': author
        })
        return result


__all__ = ['Reader', 'TemplateReader', 'HtmlReader', 'MarkdownReader', 'MagazineNcxReader', 'NcxReader', 'ImageReader']
