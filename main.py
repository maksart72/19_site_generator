import markdown
import json
import collections


CONFIG = 'config.json'

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


if __name__ == '__main__':
    sitemap = create_sitemap()
    index_content = []
    for index in sitemap:
        index_content.append((index.md_source,index.slug,index.topic_title,index.article_url))
    print(index_content)

