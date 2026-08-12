from flask import Flask, url_for, render_template
from typing import Callable, Any
from sigtemplate.templite import Templite
from anint import translations, Translator

from load_translations import load_translations


translations.load("./locales/")


app: Flask = Flask(
    __name__,
    static_folder="../../static",
    static_url_path="/static"
)
translator: Translator = Translator(
    locales=["en", "ja"],
    locale="en",
    fallbacks=["en"]
)
t: Callable[[str, tuple[Any]], str] = translator.translate


def render(locale: str, template_name: str, *contexts: Any) -> str:
    # Load webpage images
    webpage_images: list = [
        # about us images
        ("tsn_logo", "../../static/assets/images/organizer_logos/TSN_logo_blue.png"),
        ("tuj_cs_society_logo", "../../static/assets/images/organizer_logos/TUJ_CS_SOCIETY_LOGO.JPG"),
        ("gdgoc_iput_logo", "../../static/assets/images/organizer_logos/GDG-on-Campus-IPUT-Icon-Dark.png"),
        ("gdgoc_waseda_logo", "../../static/assets/images/organizer_logos/Copy of __ GDG + PA + Chapter Lockup - Centered - Template.png"),
    ]

    try:
        translator.set_locale(locale)
        with open(f"templates/{template_name}.html", "r") as f:
            html_string = f.read()
            return Templite(
                html_string,
                *[dict(map(lambda kv: (kv[0], t(kv[1])), context.items()))
                    for context in contexts],
                *[
                    dict(map(lambda image_link: (image_link[0], image_link[1]), webpage_images))
                ] # passing images as context
                ).render()
    except Exception as e:
        print(f"ERROR: {str(e)}")
        exit(1)


def render_index(locale: str) -> str:
    translations_file_path: str = "./locales/" + locale + ".yaml"
    index_translations: list[dict[str, Any]] = load_translations(translations_file_path, "index")
    return render(
        locale,
        "index",
        *index_translations
    )


def render_about(locale: str) -> str:
    translations_file_path: str = "./locales/" + locale + ".yaml"
    about_translations: list[dict[str, Any]] = load_translations(translations_file_path, "about")
    return render(
        locale,
        "about",
        *about_translations
    )


@app.route("/")
def index_en():
    return render_index("en")


@app.route("/ja/")
def index_ja():
    return render_index("ja")


@app.route("/about")
def about_en():
    return render_about("en")
