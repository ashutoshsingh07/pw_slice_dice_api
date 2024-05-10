# PW - API

A FastAPI microservice for calculating summary statistics on employee data. 

## Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)<your-username>/<your-repo-name>.git
   cd <your-repo-name>


2. **Create a virtual environment:**
   ```bash
    python -m venv env
    source env/bin/activate  

    
3. **Install dependencies:**
```
pip install -r requirements.txt
```

4. **Running the Service:**
```
cd pw_slice_and_dice
uvicorn main:app --reload

```

# API Usage Documentation

## Overview

This document outlines how to interact with our FastAPI service. Our API provides endpoints for managing employees, retrieving statistical summaries, and user authentication.

## Authentication and Authorization

To access most of the endpoints, you'll need a valid access token, which can be obtained by logging in.

### Obtaining an Access Token

### Login

**Endpoint**: `POST /login`

**Authorization**: Required

**Credentials**: The username and password should be provided using basic HTTP authentication.

**Responses**:
- **200 OK**:
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }


- **401 Unauthorized**:

    ```json
    {
    "detail": "Incorrect username or password"
    }

- **Using Access Token**:
    ```
    Include the obtained access_token in the Authorization header as a bearer token to authenticate requests to protected endpoints.
    ```
### **Note**: 
If you are using postman, go to auth, select basic auth there in ``username`` enter ``ashutosh`` and in ``password`` enter ``ashutosh``



## Other Endpoints

#### Root Endpoint

Endpoint: GET /

Authorization: None

Description: Returns the currently loaded dataset.



#### Add Employee
Endpoint: POST /employee

Authorization: `Bearer Token`

Body:

```json
{
"name": "string",
"department": "string",
"salary": "number",
"on_contract": "boolean"
}
```
Responses:

200 OK:
```json
{
"message": "Employee added"
}
```

#### Delete Employee
Endpoint: DELETE /employee/{name}

Authorization: `Bearer Token`

Responses:

200 OK:
```json
{
  "message": "Employee deleted"
}
```
404 Not Found:
```json

{
  "detail": "Employee not found"
}
```

### Statistical Summaries
#### Overall Summary
Endpoint: GET /summary

Authorization: None

Description: Returns statistical summaries of the entire dataset.

#### Summary by Contract
Endpoint: GET /summary/contract

Authorization: None

Description: Returns summaries for employees who are on contract.

#### Summary by Department
Endpoint: GET /summary/department

Authorization: None

Description: Provides a detailed breakdown of salary statistics by department.

#### Salary Statistics by Department and Sub-department
Endpoint: GET /summary/department-subdepartment

Authorization: None

Description: Calculates salary statistics for each combination of department and sub-department.

### Common Errors
    401 Unauthorized: Authentication failed, possibly due to invalid credentials.

    404 Not Found: The requested resource or endpoint is not available.



### Dataset
    The dataset is initially loaded from a file named dataset.json located in the root of the project.

### Testing
You can use your favorite tool (e.g., Postman, Insomnia, curl) to send requests to the endpoints and test the service.

## Running the Tests

The project includes basic tests using pytest. To run the tests:
```
From the project's root directory, execute: `pytest test_api.py/`
```