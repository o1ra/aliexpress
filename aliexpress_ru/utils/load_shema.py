import os
import json

main_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def load_schema(filepath):
    with open(os.path.join(main_path, 'schemas', f"{filepath}")) as file:
        schema = json.load(file)
        print(file)
        return schema




import jsonschema

#
# def load_schema(filepath):
#     with open(filepath) as file:
#         schema = json.load(file)
#         return schema