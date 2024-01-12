import os
import json

main_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def load_path(filepath):
    full_path = os.path.join(main_path, 'schemas', filepath)
    print(f"Full path to the file: {full_path}")
    with open(full_path) as file:

        schema = json.load(file)
        return schema


