import markdown
import json
import collections


source = '1_python_basics'

def load_article(source):
    Article = collections.namedtuple('Article', 'text title slug')
    with open('articles/'+source, 'r', encoding='utf-8') as file:
        html = markdown.markdown(file.read())

    json_sitemap = load_sitemap()
    for top in json_sitemap['articles']:
        if top['source'] == source:
            title = top['title']
            topic = top['topic']

    content = Article(text=html, title=title, slug=topic)
    return content




def load_sitemap():
    with open('config.json','r', encoding='utf-8') as config:
        sitemap = json.load(config)
    return sitemap

def index():

    json_sitemap = load_sitemap()
    sitemap = []
    source = '1_python_basics'
    for url in json_sitemap['articles']:
        article_info = (url['source'].split('/')[0],url['source'].split('/')[1].split('.')[0], url['title'])
        sitemap.append(article_info)



    category_list = json_sitemap['topics']
    for slug in category_list:
        print(str(source.split('_')[1]))
    #   if slug['slug'] == str(source.split('_')[1]):
    #       category = slug['title']
    return(None)

if __name__ == '__main__':
    source = '0_tutorial/14_google.md'
    article = load_article(source)
    print(article)
    print(load_sitemap())
    print(index())

