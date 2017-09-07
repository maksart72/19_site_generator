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

def html_special_chars(text):
    return text \
    .replace(u'"', u"&quot;") \
    .replace(u"'", u"&#039;") \
    .replace(u"<", u"&lt;") \
    .replace(u">", u"&gt;")

def load_json_config():
    with open(CONFIG, 'r', encoding='utf-8') as config:
        json_site_map = json.load(config)
    return json_site_map

def create_site_map():
    content = []
    json_site_map = load_json_config()
    site_map = collections.namedtuple(
        'site_map', 'md_source slug topic_title article_url article_title html_content')
    for articles in json_site_map['articles']:
        md_source = articles['source']
        slug = articles['topic']
        article_title = html_special_chars(articles['title'])
        article_url = articles['source'].split('/')[1][:-3].replace(u' ', u"%20")
        with open('articles/' + md_source, 'r', encoding='utf-8') as file:
            html_content = markdown.markdown(file.read())
        for topics in json_site_map['topics']:
            if topics['slug'] == slug:
                topic_title = topics['title']
        content.append(site_map(md_source=md_source, slug=slug, topic_title=topic_title,
                                article_url=article_url, article_title=article_title, html_content=html_content),)
    return content


def create_site_folders(json_site_map):
    if not os.path.exists(SITE_ROOT):
        os.makedirs(SITE_ROOT)
    for slug in json_site_map['topics']:
        article_dir = os.path.join(SITE_ROOT, slug['slug'])
        if not os.path.exists(article_dir):
            os.makedirs(article_dir)


def get_jinja2_template(filename, path):
    env = Environment(loader=FileSystemLoader(path))
    return env.get_template(filename)


def save_html(path, article_html):
    with open(path, 'w', encoding=ENCODING) as html_file:
        html_file.write(article_html)


def generate_index(site_map):
    index_content = []
    for index in site_map:
        index_content.append((index.md_source, index.slug,
                              index.topic_title, index.article_url, index.article_title))
    return index_content


def save_index(index_content):
    index_template = get_jinja2_template('index.html', TEMPLATES_PATH)
    path_index = SITE_ROOT + '/' + 'index.html'
    index_html = index_template.render(index_content=index_content)
    save_html(path_index, index_html)


def generate_category(topic):
    site_map = create_site_map()
    generated_topic_content = []
    generated_topics_title = 'None'
    for topics in site_map:
        if topics.slug == topic:
            generated_topic_content.append(
                (topics.md_source, topics.slug, topics.topic_title, topics.article_url, topics.article_title))
            generated_topics_title = topics.topic_title
    return generated_topic_content, generated_topics_title


def save_category(json_site_map):
    category_template = get_jinja2_template('category.html', TEMPLATES_PATH)
    for topic in json_site_map['topics']:
        topic_content, topics_title = generate_category(topic['slug'])
        path_category = SITE_ROOT + '/' + topic['slug'] + '/index.html'
        category_html = category_template.render(
            topics=topic_content, topic_title=topics_title)
        save_html(path_category, category_html)


def generate_html(site_map):
    article_template = get_jinja2_template('article.html', TEMPLATES_PATH)
    for article in site_map:
        article_html = article_template.render(md_source=article.md_source, slug=article.slug,
                                               topic_title=article.topic_title, article_url=article.article_url,
                                               article_title=article.article_title, html_content=article.html_content)
        path = SITE_ROOT + '/' + article.slug + '/' + article.article_url + '.html'
        save_html(path, article_html)


# Flask setup
app = Flask(__name__)


@app.route("/")
def index():
    index_content = generate_index(site_map)
    return render_template("index.html",
                           index_content=index_content)


@app.route('/<topic>/')
def view_topics(topic):
    topic_content, topics_title = generate_category(topic)
    return render_template('category.html', topics=topic_content, topic_title=topics_title)


@app.route('/<topic>/<article_url>.html')
def view_article(topic=None, article_url=None):
    site_map = create_site_map()
    for article in site_map:
        if article.article_url == article_url:
            return render_template('article.html', md_source=article.md_source, slug=article.slug,
                                   topic_title=article.topic_title, article_url=article.article_url,
                                   article_title=article.article_title, html_content=article.html_content)


if __name__ == '__main__':

    json_site_map = load_json_config()
    create_site_folders(json_site_map)
    site_map = create_site_map()
    generate_html(site_map)
    index_content = generate_index(site_map)
    save_index(index_content)
    save_category(json_site_map)
    app.run(debug=True, use_reloader=True)

