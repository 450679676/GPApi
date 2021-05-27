import yaml


def read_yaml(filename="./data/todo_list.yaml"):
    with open(filename, 'r', encoding='utf-8') as f:
        return list(yaml.safe_load_all(f))
