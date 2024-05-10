import json
from unittest.mock import patch
import numpy as np
import pytest
from fastapi.testclient import TestClient

from models import Employee

from utils import load_dataset, save_dataset, calculate_summary_stats
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == load_dataset()

def test_add_employee():
    employee = Employee(name="John Doe", department="Engineering", salary=100000)
    response = client.post("/employee", json=employee.dict())
    assert response.status_code == 401

def test_delete_employee():
    employee = Employee(name="John Doe", department="Engineering", salary=100000)
    save_dataset([employee.dict()])
    response = client.delete("/employee/John Doe")
    assert response.status_code == 401

def test_get_overall_summary():
    data = [
        {"name": "John Doe", "department": "Engineering", "sub_department": "Backend", "salary": 100000},
        {"name": "Jane Doe", "department": "Sales", "sub_department": "Marketing", "salary": 80000},
        {"name": "Bob Smith", "department": "Engineering", "sub_department": "Frontend", "salary": 90000},
        {"name": "Alice Johnson", "department": "Sales", "sub_department": "Marketing", "salary": 70000},
    ]
    save_dataset(data)
    response = client.get("/summary")
    assert response.status_code == 200
    
    assert response.json() == {'mean_salary': 85000.0, 'min_salary': 70000.0, 'max_salary': 100000.0}