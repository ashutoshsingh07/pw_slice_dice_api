import json
from collections import defaultdict

import numpy as np
from fastapi import FastAPI, HTTPException, Depends
from utils import load_dataset, save_dataset, calculate_summary_stats
from models import Employee
from security import authenticate_user, create_access_token, security
from fastapi.security import HTTPBasicCredentials, OAuth2PasswordBearer


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

data = load_dataset()

@app.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(security)):  
    user = authenticate_user(credentials)  
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/")
async def read_root():
    return data

@app.post("/employee")
async def add_employee(employee: Employee, token: str = Depends(oauth2_scheme)):
    data.append(employee.dict())
    save_dataset(data)
    return {"message": "Employee added"}

@app.delete("/employee/{name}")
async def delete_employee(name: str, token: str = Depends(oauth2_scheme)):
    global data
    new_data = [d for d in data if d['name'] != name]
    if len(new_data) == len(data):
        raise HTTPException(status_code=404, detail="Employee not found")
    data = new_data
    save_dataset(data)
    return {"message": "Employee deleted"}

@app.get("/summary")
async def get_overall_summary():
    return calculate_summary_stats(data)

@app.get("/summary/contract")
async def get_summary_by_contract():
    filtered_data = [d for d in data if 'on_contract' in d and d['on_contract']]
    return calculate_summary_stats(filtered_data)


@app.get("/summary/department")
async def get_summary_by_department():
    result = defaultdict(dict)
    for record in data:
        department = record['department']
        salary = float(record['salary'])  # Attempt to convert salary

        if department and salary:  # Check if both exist
            if "count" not in result[department]:
                result[department]["count"] = 0  # Initialize
                result[department]["sum"] = 0
                result[department]["min"] = float('inf')  # Set min to high value
                result[department]["max"] = float('-inf') # Set max to low value

            result[department]["count"] += 1
            result[department]["sum"] += salary
            result[department]["min"] = min(result[department]["min"], salary)
            result[department]["max"] = max(result[department]["max"], salary)

    # Calculate means
    for department, stats in result.items():
        if stats["count"] > 0:  # Protect against division by zero
            stats["mean"] = stats["sum"] / stats["count"] 

    return result 

@app.get("/summary/department-subdepartment")
async def get_salary_stats_for_department_sub_department():

    dataset = load_dataset()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset is empty")

    # Calculate salary statistics for each department and sub-department combination
    department_sub_department_stats = defaultdict(lambda: {
        "count": 0, "sum": 0.0, "min": float('inf'), "max": float('-inf')
    })
    for employee in dataset:
        department = employee.get("department")
        sub_department = employee.get("sub_department")

        if department and sub_department:

            key = f"{department}-{sub_department}"

            salary = float(employee.get("salary"))

            if salary:

                if "count" not in department_sub_department_stats[key]:
                    department_sub_department_stats[key]["count"] = 1
                    department_sub_department_stats[key]["sum"] = salary
                    department_sub_department_stats[key]["min"] = salary
                    department_sub_department_stats[key]["max"] = salary

                else:

                    department_sub_department_stats[key]["count"] += 1
                    department_sub_department_stats[key]["sum"] += salary
                    department_sub_department_stats[key]["min"] = min(department_sub_department_stats[key]["min"],
                                                                      salary)
                    department_sub_department_stats[key]["max"] = max(department_sub_department_stats[key]["max"],
                                                                      salary)



    # Calculate mean salary for each department and sub-department combination
    for key, stats in department_sub_department_stats.items():
        stats["mean"] = stats["sum"] / stats["count"]
    return department_sub_department_stats