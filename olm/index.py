import os
import datetime
import codecs
import re
import math
from helper import md_parse_meta

class Index:
    """Object representing an index listing"""

    def __init__(self, context):
        self.context = context
        all_files = sorted(context.ARTICLES, key=lambda k: (k.date), reverse=True)
        self.articles = [ article for article in all_files if article.type in (context.ARTICLE_TYPES + context.INDEX_TYPES) ]
        self.template = context.JINJA_ENV.get_template('index.html')
        self.output_filepath = os.path.join(context.OUTPUT_FOLDER, 'index.html')
        self.paginate()

    def paginate(self):
        num_per_page = 10
        num_pages = math.ceil(len(self.articles)/num_per_page)
        pages = []
        articles = self.articles
        for i in range(0, num_pages):
            page_articles = articles[0:num_per_page]
            articles = articles[num_per_page:]
            pages.append(page_articles)
        self.pages = pages

    def paginated_path(self, page_number, basepath):
        if page_number == 1:
            return os.path.join(basepath, 'index.html'), '/'
        return os.path.join(self.context.OUTPUT_FOLDER,'pg', str(page_number) , 'index.html'), os.path.join('/', 'pg', str(page_number))


    def write_file(self):
        """Write the article to a file"""
        dirname = os.path.dirname(self.output_filepath)
        for i, page in enumerate(self.pages):
            page_number = i + 1
            output_filepath, url = self.paginated_path(page_number, dirname)
            previous_page = None
            next_page = None
            if i > 0: 
                previous_filepath, previous_page = self.paginated_path(page_number - 1, dirname)
            if i < len(self.pages):
                next_filepath, next_page = self.paginated_path(page_number + 1, dirname)
            os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
            with codecs.open(output_filepath, 'w', encoding='utf-8') as html_file:
                html = self.template.render(
                    articles=self.articles, 
                    pages=self.pages, 
                    page=page,
                    previous_page=previous_page,
                    next_page=next_page,
                    **self.context)
                html_file.write(html)