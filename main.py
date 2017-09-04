import markdown
import json
import collections
import os

SITE_ROOT = "site"
source = '0_tutorial/27_devman.md'
CONFIG_PATH = "config.json"

def load_article(article_url):
    json_sitemap = load_sitemap()
    for articles in json_sitemap['articles']:
        print(articles['source'].split('/')[1][:-3])
        if articles['source'].split('/')[1][:-2] == article_url:
            title = articles['title']
            topic = articles['topic']
            source = articles['source']
    Article = collections.namedtuple('Article', 'text title slug')
    with open('articles/'+source, 'r', encoding='utf-8') as file:
        html = markdown.markdown(file.read())
    content = Article(text=html, title=title, slug=topic)
    return content


def load_sitemap():
    with open('config.json','r', encoding='utf-8') as config:
        sitemap = json.load(config)
    return sitemap


def create_site_folders(json_sitemap):
    if not os.path.exists(SITE_ROOT):
        os.makedirs(SITE_ROOT)

    for slug in json_sitemap['topics']:
        article_dir = os.path.join(SITE_ROOT, slug['slug'])
        print(article_dir)
        if not os.path.exists(article_dir):
            os.makedirs(article_dir)


if __name__ == '__main__':

    load_file(source)
    print(load_article(article_url=''))
    sitemap = load_sitemap()
    print(sitemap)
    create_site_folders(sitemap)

