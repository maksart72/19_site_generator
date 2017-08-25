import markdown
import json
from flask import Flask, render_template
app = Flask(__name__)





def load_article():
    with open('articles/1_python_basics/1_intro.md', 'r', encoding='utf-8') as file:
        html = markdown.markdown(file.read())
    return html

def load_sitemap():
    with open('config.json','r', encoding='utf-8') as config:
        sitemap = json.load(config)
    return sitemap

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/view")
def template_test():
    article = load_article()
    return render_template('template.html', article = article)


if __name__ == '__main__':
    app.run(debug=True)
