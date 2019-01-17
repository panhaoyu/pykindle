from pykindle import items


def test_get_field():
    item = items.Item()
    item.id = "test_id"
    assert isinstance(item.id, str)


def test_get_empty_field():
    item = items.Item()
    try:
        i = item.id
        raise AssertionError
    except items.FieldNotSetError:
        pass


def test_get_default_field():
    item = items.MarkdownArticleItem()
    assert isinstance(item.title, str)


def test_get_non_exist_field():
    item = items.NcxItem()
    try:
        nothing = item.it_is_not_an_item
        assert 0
    except AttributeError:
        pass


def test_set_field_twice():
    item = items.Item()
    item.href = 'path/to/item'
    item.href = 'path/to/item'
    assert item.href == 'path/to/item'


def test_get_field_twice():
    item = items.Item()
    item.href = 'path/to/item'
    assert item.href == 'path/to/item'
    assert item.href == 'path/to/item'


def test_set_readonly_field():
    item = items.Item()
    try:
        item.content = 'nothing'
        assert 0
    except AttributeError:
        pass


def test_item():
    item = items.Item()
    item.href = 'path/to/item'
    assert item.href == 'path/to/item'
    item.media_type = 'application/xhtml+xml'
    assert item.media_type == 'application/xhtml+xml'
    item.id = 'temp_id'
    assert item.id == 'temp_id'
    item.source = 'This is a source line.'
    assert item.source == 'This is a source line.'


def test_article():
    item = items.ArticleItem()
    assert isinstance(item.title, str)
    assert isinstance(item.author, str)
    assert isinstance(item.description, str)
    assert isinstance(item.category, str)
    item.title = 'this is a title'
    assert item.title == 'this is a title'
    item.author = 'this is a author'
    assert item.author == 'this is a author'
    item.description = 'this is a description'
    assert item.description == 'this is a description'
    item.category = 'category'
    assert item.category == 'category'


def test_ncx_item():
    item = items.NcxItem()
    assert isinstance(item.title, str)
    assert isinstance(item.author, str)
    assert isinstance(item.id, str)
    assert isinstance(item.href, str)
    item.id = 'id'
    assert item.id == 'id'
    item.href = 'href'
    assert item.href == 'href'
    item.title = 'ttt'
    assert item.title == 'ttt'
    item.author = 'aaa'
    assert item.author == 'aaa'


def test_magazine_ncx_item():
    item = items.MagazineNcxItem()
    item.categories = list()
    item.categories = [('test_category', [
        items.ArticleItem(), items.ArticleItem()
    ]), ]
    assert item.categories[0][0] == 'test_category'
    item.categories = [
        ('test_category', [items.ArticleItem(), items.ArticleItem()]),
        ('test_category2', [items.ArticleItem(), items.ArticleItem()]),
        ('test_category3', [items.ArticleItem(), items.ArticleItem()]),
    ]
    assert item.categories[2][0] == 'test_category3'


def test_image_item():
    assert True


def test_reader():
    assert True


def test_write():
    assert True
