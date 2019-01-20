import asyncio
import ruia
import pykindle
import pickle


class ProblemListItem(ruia.Item):
    target_item = ruia.TextField(css_select='table table tr')
    fields = ruia.TextField(css_select='td', many=True)
    url = ruia.AttrField(css_select='a', attr='href')

    def __init__(self):
        super(ProblemListItem, self).__init__()
        self.year = None
        self.title = None
        self.student_level = None
        self.source = None
        self.commentary = None
        self.student_papers = None

    async def clean_fields(self, values):
        self.year, self.title, self.student_level, self.source, self.commentary, self.student_papers = values


class ArticleItem(ruia.Item):
    content = ruia.HtmlField(css_select='table table p', many=True)

    def clean_content(self, values):
        return '\n'.join(values)


class Spider(ruia.Spider):
    start_urls = ['http://www.mathmodels.org/problems.html']

    async def parse(self, res):
        problems = await ProblemListItem.get_items(html=res.html)
        problems = problems[1:]
        coroutines = [ArticleItem.get_item(url='http://www.mathmodels.org/' + problem.url, metadata=problem) for problem
                      in
                      problems]
        results = await asyncio.gather(*coroutines)
        with open('data.pickle', mode='wb') as file:
            pickle.dump((problems, results), file)


def book():
    with open('data.pickle', mode='rb') as file:
        problems, results = pickle.load(file)
    book = pykindle.MagazineBook()
    book.author = 'Haoyu Pan'
    book.title = 'MCM-ICM Problems'
    book.description = 'MCM and ICM problems.'
    for index, problem in enumerate(problems):
        title = problem.title
        category = problem.year
        content = results[index].content
        article = pykindle.HtmlArticleItem()
        article.description = title
        article.category = category
        article.author = 'Haoyu Pan'
        article.href = str(index) + '.html'
        article.source = content
        article.title = title
        book.append(article)
    with open('mcm.mobi', mode='wb') as file:
        file.write(book.create())


Spider.start()
book()
