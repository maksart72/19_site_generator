import markdown
import json


def load_article():
    html = markdown.markdown('# Hello!')
    return html

def load_sitemap():
    with open('config.json','r', encoding='utf-8') as config:
        sitemap = json.load(config)
    return sitemap

if __name__ == '__main__':
    print(load_sitemap())
