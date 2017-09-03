import json
import collections
import os
from livereload import Server
import markdown
from flask import (
    Flask,
    render_template)
app = Flask(__name__)
app.debug = True
server = Server(app.wsgi_app)

CONFIG_PATH = "config.json"
SITE_ROOT = "site"

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
    for topics in json_sitemap['articles']:
        if topics['source'].split('/')[1].split('.')[0] == article_url:
            title = topics['title']
            topic = topics['topic']
            source = topics['source']
    Article = collections.namedtuple('Article', 'text title slug')
    with open('articles/'+source, 'r', encoding='utf-8') as file:
        html = markdown.markdown(file.read())
    content = Article(text=html, title=title, slug=topic)
    return content

def load_sitemap():
    with open(CONFIG_PATH,'r', encoding='utf-8') as config:
        sitemap = json.load(config)
    return sitemap

def make_site():
    # TODO convert markdown to html, create site
    print('Changes founded!')
    return

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
    return render_template('article.html', article = article.text, title=article.title, slug=article.slug)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
    server.watch('templates/*.html', make_site)
    server.watch('articles/*.md', make_site)
    server.serve(root='site/')
