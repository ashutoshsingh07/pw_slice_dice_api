import json
from statistics import mean 

DATA_FILE = "dataset.json"
from fastapi import HTTPException


def load_dataset():
    try:
        with open('dataset.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_dataset(dataset):
    with open('dataset.json', 'w') as f:
        json.dump(dataset, f, indent=4)

def calculate_summary_stats(data):
    if data:
        salaries = [float(d['salary']) for d in data]
        return {
            "mean_salary": mean(salaries),
            "min_salary": min(salaries),
            "max_salary": max(salaries)
        }
    else:
        raise HTTPException(status_code=404, detail="Dataset is empty")

