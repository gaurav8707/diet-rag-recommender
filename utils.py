import pandas as pd
import json

def load_csv(path):
    return pd.read_csv(path)

def load_jsonl(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]

