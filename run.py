import json
import collections
import os
import markdown
from flask import (
    Flask,
    render_template)
from jinja2 import Environment, FileSystemLoader

SITE_ROOT = "site"
TEMPLATES_PATH = 'templates'
CONFIG = 'config.json'
ENCODING = 'utf-8'


def load_json_config():
    with open(CONFIG,'r', encoding='utf-8') as config:
        json_sitemap = json.load(config)
    return json_sitemap

def create_sitemap():
    content = []
    json_sitemap = load_json_config()
    Sitemap = collections.namedtuple('Sitemap', 'md_source slug topic_title article_url article_title html_content')
    for articles in json_sitemap['articles']:
        md_source = articles['source']
        slug = articles['topic']
        article_title=articles['title']
        article_url = articles['source'].split('/')[1][:-3]
        with open('articles/' + md_source, 'r', encoding='utf-8') as file:
            html_content = markdown.markdown(file.read())
        for topics in json_sitemap['topics']:
            if topics['slug'] == slug:
                topic_title = topics['title']
        content.append(Sitemap(md_source = md_source, slug = slug ,topic_title = topic_title, article_url = article_url ,article_title = article_title, html_content = html_content),)
    return content

def create_site_folders(json_sitemap):
    if not os.path.exists(SITE_ROOT):
        os.makedirs(SITE_ROOT)
    for slug in json_sitemap['topics']:
        article_dir = os.path.join(SITE_ROOT, slug['slug'])
        if not os.path.exists(article_dir):
            os.makedirs(article_dir)

def get_jinja2_template(filename, path):
    env = Environment(loader=FileSystemLoader(path))
    return env.get_template(filename)


def save_html(path, article_html):
    with open(path, 'w') as html_file:
        html_file.write(article_html)

def generate_index(sitemap):
    index_content = []
    for index in sitemap:
        index_content.append((index.md_source,index.slug,index.topic_title,index.article_url,index.article_title))
    return index_content

def save_index(index_content):
    index_template = get_jinja2_template('index.html', TEMPLATES_PATH)
    path_index = SITE_ROOT + '/' + 'index.html'
    index_html = index_template.render(index_content = index_content)
    save_html(path_index, index_html)


def generate_html(sitemap):
    article_template = get_jinja2_template('article.html', TEMPLATES_PATH)
    #category_template = get_jinja2_template('category.html', TEMPLATES_PATH)
    for article in sitemap:
        article_html = article_template.render(md_source=article.md_source, slug=article.slug,
                                               topic_title=article.topic_title, article_url=article.article_url,
                                               article_title=article.article_title, html_content=article.html_content)
        path = SITE_ROOT + '/' + article.slug + '/' + article.article_url + '.html'
        save_html(path, article_html)

# Flask setup
app = Flask(__name__)

@app.route("/")
def index():
    index_content = generate_index(sitemap)
    return render_template("index.html",
                       index_content=index_content)

'''
@app.route('/<topic>/')
def view_topics(topic):
    json_sitemap = load_sitemap()
    sitemap = []
    category = 'basics'
    for url in json_sitemap['articles']:
        if url['topic'] == topic:
            article_info = (url['topic'],url['source'].split('/')[1][:-3], url['title'])
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
'''
if __name__ == '__main__':

    json_sitemap = load_json_config()
    sitemap = create_sitemap()
    create_site_folders(json_sitemap)
    generate_html(sitemap)

    index_content = generate_index(sitemap)
    save_index(index_content)

    app.run(debug=True, use_reloader=True)