# pykindle
A library to make book.mobi files.

Kindlegen packaged all the functions in a file,
 and here we'd like to develop it's python API.

# Install

`pip install pykindle`

# Usage

```python
import pykindle
book = pykindle.Magazine()
article = pykindle.MarkdownArticleItem()
article.href = 'page1.html'
article.source = 'This is a page.'
book.append(article)
book_bytes = book.create()
with open('output.mobi', mode='wb') as file:
    file.write(book_bytes)
```

For example, click [here][magazine_example].

# Not finished yet

There are so many functions that haven't been implemented yet.

Currently, PyKindle only support to generate a magazine format book without photos.

[magazine_example]: https://github.com/panhaoyu/pykindle/blob/master/tests/test_magazine.py

