import json
import collections
import os
import markdown
from flask import (
    Flask,
    render_template)
from jinja2 import Environment, FileSystemLoader

SITE_ROOT = "site"
OUTPUT_SITE_PATH = 'site'
ARTICLES_PATH = 'articles'
TEMPLATES_PATH = 'templates'
INDEX_FILE = 'index.html'
CONFIG = 'config.json'
ENCODING = 'utf-8'

app = Flask(__name__)

def get_jinja_template(filename, path):
    env = Environment(loader=FileSystemLoader(path),
                      auto_reload=True,
                      trim_blocks=True,
                      lstrip_blocks=True,)
    return env.get_template(filename)

def create_site_folders(json_sitemap):
    if not os.path.exists(SITE_ROOT):
        os.makedirs(SITE_ROOT)

    for slug in json_sitemap['topics']:
        article_dir = os.path.join(SITE_ROOT, slug['slug'])
        print(article_dir)
        if not os.path.exists(article_dir):
            os.makedirs(article_dir)

def load_article(article_url):
    json_sitemap = load_sitemap()
    for articles in json_sitemap['articles']:
        if articles['source'].split('/')[1][:-3] == article_url:
            title = articles['title']
            topic = articles['topic']
            source = articles['source']
    for topics in json_sitemap['topics']:
        if topics['slug'] == topic:
            topic_title = topics['title']
    Article = collections.namedtuple('Article', 'text title slug topic_title')
    with open('articles/'+source, 'r', encoding='utf-8') as file:
        html = markdown.markdown(file.read())
    content = Article(text=html, title=title, slug=topic, topic_title= topic_title)
    return content


def return_html_from_md(source):
    Article = collections.namedtuple('Article', 'text title slug topic_title')
    json_sitemap = load_sitemap()
    for articles in json_sitemap['articles']:
        if articles['source'] == source:
            title = articles['title']
            topic = articles['topic']
    for topics in json_sitemap['topics']:
        if topics['slug'] == topic:
            topic_title = topics['title']
    with open('articles/' + source, 'r', encoding='utf-8') as file:
        html = markdown.markdown(file.read())

    content = Article(text=html, title=title, slug=topic, topic_title = topic_title)
    return content


def load_sitemap():
    with open(CONFIG,'r', encoding='utf-8') as config:
        sitemap = json.load(config)
    return sitemap


def generate_html():
    json_sitemap = load_sitemap()
    for articles in json_sitemap['articles']:
        path = SITE_ROOT+'/'+articles['topic']+'/'+articles['source'].split('/')[1].replace('.md', '.html')
        source = articles['source']
        article_template = get_jinja_template('article.html', TEMPLATES_PATH)
        content = return_html_from_md(source)
        article_html = article_template.render(article=content.text, title = content.title, slug = content.slug,
                                               topic_title = content.topic_title)
        save_html(path, article_html)

def save_html(path, article_html):
    with open(path, 'w') as html_file:
        html_file.write(article_html)

@app.route("/")
def index():
    json_sitemap = load_sitemap()
    sitemap = []
    for url in json_sitemap['articles']:
        article_info = (url['topic'],url['source'].split('/')[1].split('.')[0], url['title'])
        sitemap.append(article_info)
    return render_template("index.html",
                       articles=sitemap)


@app.route('/<topic>/')
def view_topics(topic):
    json_sitemap = load_sitemap()
    sitemap = []
    category = 'basics'
    for url in json_sitemap['articles']:
        if url['topic'] == topic:
            article_info = (url['topic'],url['source'].split('/')[1].split('.')[0], url['title'])
            sitemap.append(article_info)
    category_list = json_sitemap['topics']
    for slug in category_list:
        if slug['slug'] == topic:
            category = slug['title']
    return render_template("category.html",
                       articles=sitemap, category = category)

@app.route('/<topic>/<article_url>')
def view_article(topic=None, article_url=None):
    article = load_article(article_url)
    return render_template('article.html', article = article.text, title=article.title, slug=article.slug, topic_title = article.topic_title)

if __name__ == '__main__':


    sitemap = load_sitemap()
    create_site_folders(sitemap)
    generate_html()
    app.run(debug=True, use_reloader=True)