from anint import translations
from flask import Flask, redirect
from sigtemplate.templite import Templite


translations.load("locales/")


app: Flask = Flask(
    __name__,
    static_folder="../../static",
    static_url_path="/static"
)


def render(locale: str, template_name: str) -> str:
    with open(f"templates/{template_name}.html", "r") as f:
        return Templite(f.read(), translations.data[locale]).render()


def render_index(locale: str) -> str:
    return render(locale, "index")


def render_about(locale: str) -> str:
    return render(locale, "about")


@app.route("/")
def redirect_index():
    return redirect("/en/")


@app.route("/en/")
def index_en():
    return render_index("en")


@app.route("/ja/")
def index_ja():
    return render_index("ja")


@app.route("/en/about")
def about_en():
    return render_about("en")


@app.route("/ja/about")
def about_ja():
    return render_about("ja")
