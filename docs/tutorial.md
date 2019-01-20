# Tutorial

## Install

```cmd
pip install pykindle
```

## Usage

```python
import pykindle

# Create a book object.
book = pykindle.MagazineBook()

# Create articles.
article1 = pykindle.MarkdownArticleItem()
article1.href = 'article1.html'
article1.category = 'category1'

article2 = pykindle.MarkdownArticleItem()
article2.href='article2.html'
article2.category = 'category1'

article3 = pykindle.MarkdownArticleItem()
article3.href = 'article3.html'
article3.category = 'category2'

# Attach articles to the book.
book.append(article1)
book.append(article2)
book.append(article3)

# Get book byte content
book_as_byte = book.create()

# Save the book, or send the book to your kindle mailbox
with open('my_book.mobi',mode='wb') as file:
    file.write(book_as_byte)

```


The example is saved [here][source]

[source]: https://github.com/panhaoyu/pykindle/blob/master/examples/create_magazine.py

