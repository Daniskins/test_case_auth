import json
import os
from json import JSONDecodeError

curr_dir = os.path.dirname(__file__)
js_path = os.path.join(curr_dir, '..', 'database', 'sessions.json')

def read_json() -> dict:
    if not os.path.exists(js_path):
        return {'seq': 0, 'sessions': []}
    try:
        with open(js_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except JSONDecodeError:
        return {'seq': 0, 'sessions': []}

def write_json(data: dict) -> None:
    with open(js_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
