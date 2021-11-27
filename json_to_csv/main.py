import csv
import json

from pathlib import Path
from typing import List

file_name = 'dk_mouth'
target_json_dir = f'smoke/{file_name}.json'
csv_dir = 'static/csv'


def get_json_path() -> str:
    cwd = Path.cwd()
    return str(cwd.parent / target_json_dir)


def get_csv_path() -> str:
    cwd = Path.cwd()
    return str(cwd.parent / csv_dir)


def read_json(target_dir) -> List:
    with open(target_dir) as json_file:
        return json.load(json_file)


def write_csv(path: str, data: List):
    cols = data[0].keys()
    with open(f"{path}/{file_name}.csv", 'w') as f:
        wr = csv.DictWriter(f, fieldnames=cols)
        wr.writeheader()
        wr.writerows(data)


def generate_folder_if_does_not_exist(path):
    Path(path).mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    json_data = read_json(get_json_path())
    csv_path = get_csv_path()
    generate_folder_if_does_not_exist(csv_path)
    write_csv(path=csv_path, data=json_data)
