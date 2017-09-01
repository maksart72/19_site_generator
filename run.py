import json
import collections
from livereload import Server
import markdown
from flask import (
    Flask,
    render_template)
app = Flask(__name__)

CONFIG_PATH = "config.json"

def load_article(article_url):

    json_sitemap = load_sitemap()
    for top in json_sitemap['articles']:
        if top['source'].split('/')[1].split('.')[0] == article_url:
            title = top['title']
            topic = top['topic']
            source = top['source']

    Article = collections.namedtuple('Article', 'text title slug')
    with open('articles/'+source, 'r', encoding='utf-8') as file:
        html = markdown.markdown(file.read())

    content = Article(text=html, title=title, slug=topic)
    return content


def load_sitemap():
    with open(CONFIG_PATH,'r', encoding='utf-8') as config:
        sitemap = json.load(config)
    return sitemap


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
    return render_template('article.html', article = article.text, title=article.title, slug=article.slug)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
