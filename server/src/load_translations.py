"""Loads translations required for each website based on the nested YAML structure.

Example:    
    If the file stores 
    ```yaml
    index:
        word: translation
    ```
    It loads every translation for that page, provided the name of the page, and 
    that the name is available in the yaml config file.
"""

import os
import yaml
from typing import Any


def load_yaml_file(file_path: str) -> dict[str, Any]:
    """Safe loads the provided yaml translations file.

    Raises:
        FileNotFoundError if the translations file doesn't exist on disk.

    Args:
        filename: str : file name of yaml translations config file

    Returns:
        dictionary of {word: translation} pairs.
    
    """
    # check if file exists
    if (not os.path.isfile(file_path)):
        raise FileNotFoundError("load_translations(): file wasn't found on disk:", file_path)

    with open(file_path, "r", encoding="utf8") as file:
            return yaml.safe_load(file)


def load_translations(
        file_path: str, template_name: str
    ) -> list[dict[str, Any]]:
    """Loads translations into dictionaries of word, translation pairs from provided 
    translation yaml file

    Args:
        file_path: str : file path of translations yaml file
        template_name: str : root level object name to load translations frmo

    Returns:
        list of (template_name, template_name.word) dictionaries that can be later unpacked as context to pass 
        into a templating engine.

    """
    translations: dict[str, Any] = load_yaml_file(file_path)

    # template_name / web_page_name wasn't found in the translations file
    if (template_name not in translations):
        print("Template name not found at the root level of the translations file.")
        exit(1)

    # TODO: In the future, just add the translations directly
    # Note: Ankha, I didn't want to remove your masterpiece, so let's keep it inefficient for now

    # make a list of tuple(template_name, template_name.word) pairs
    unpacked_translations: list[dict[str, Any]] = []
    for word in translations[template_name]:
        unpacked_translations.append(
            {word: template_name + '.' + word}
        )
    
    return unpacked_translations
