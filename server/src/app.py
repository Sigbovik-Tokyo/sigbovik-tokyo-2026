from flask import Flask
from typing import Callable, Any
from sigtemplate.templite import Templite
from anint import translations, Translator


translations.load("./locales/")


app: Flask = Flask(__name__)
translator: Translator = Translator(
    locales=["en", "ja"],
    locale="en",
    fallbacks=["en"]
)
t: Callable[[str, tuple[Any]], str] = translator.translate


def render(locale: str, template_name: str, *contexts: Any) -> str:
    try:
        translator.set_locale(locale)
        with open(f"templates/{template_name}.html", "r") as f:
            html_string = f.read()
            return Templite(
                html_string,
                *[dict(map(lambda kv: (kv[0], t(kv[1])), context.items()))
                    for context in contexts]
                ).render()
    except Exception as e:
        print(f"ERROR: {str(e)}")
        exit(1)


def render_index(locale: str) -> str:
    return render(
        locale,
        "index",
        {"lang": "index.lang"},
        {"title": "index.title"},
        {"body": "index.body"},
    )


@app.route("/")
def index_en():
    return render_index("en")


@app.route("/ja/")
def index_ja():
    return render_index("ja")
