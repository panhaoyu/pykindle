import os
import markdown
import jinja2

_template_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')


class Reader(object):
    def render(self, *args, **kwargs):
        pass


class TemplateReader(Reader):
    def __init__(self, jinja2_loader=jinja2.FileSystemLoader(_template_dir)):
        self._jinja2 = jinja2.Environment(loader=jinja2_loader)


class HtmlReader(TemplateReader):
    def render(self, title, author, description, content):
        super(HtmlReader, self).render()
        template = self._jinja2.get_template('article.html')
        return template.render({
            'title': title,
            'author': author,
            'description': description,
            'content': content,
        })


class MarkdownReader(HtmlReader):
    def __init__(self, markdown_options=None, **kwargs):
        super(MarkdownReader, self).__init__(**kwargs)
        self._markdown_options = markdown_options if markdown_options else dict()

    def render(self, title, author, description, content):
        content = markdown.markdown(content, **self._markdown_options)
        return super(MarkdownReader, self).render(title, author, description, content)


class ImageReader(Reader):
    def render(self, content):
        return content


class NcxReader(TemplateReader):
    pass


class MagazineNcxReader(NcxReader):
    def render(self, categories, title, author):
        template = self._jinja2.get_template('magazine.ncx')
        result = template.render({
            'categories': categories,
            'title': title,
            'author': author
        })
        return result
