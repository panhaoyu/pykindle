import os
import glob
import tempfile
import pykindle


def test_magazine():
    book = pykindle.Magazine()
    base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
    contents = {
        '技术领导力300讲': [
            '开篇词：卓越的团队，必然有一个卓越的领导者',
            '第1讲：你的能力模型决定你的职位',
            '大咖对话：从几个工程师到2000more个工程师的技术团队成长秘诀',
            '第14讲：从零开始搭建轻量级研发团队',
        ],
        '硅谷产品实战36讲': [
            '开篇词：打造千万用户的世界级产品',
            '01：什么是优秀的产品经理？',
            '02：硅谷的产品经理是什么样子的？',
        ]
    }
    for category, articles in contents.items():
        for article_file_name in articles:
            path = os.path.join(base_path, '{}.html'.format(article_file_name))
            with open(path, mode='r', encoding='utf-8') as file:
                content = file.read()
            article = pykindle.HtmlArticleItem()
            article.category = category
            article.title = article_file_name
            article.source = content
            article.href = os.path.split(path)[1]
            book.append(article)
    content = book.create()
    with tempfile.TemporaryDirectory() as directory:
        with open(os.path.join(directory, 'output.mobi'), mode='wb') as file:
            file.write(content)
