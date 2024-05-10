from pydantic import BaseModel

class Employee(BaseModel):
    name: str
    salary: float  # Assuming USD if currency not specified
    currency: str = "USD"
    department: str
    on_contract: bool = False
    sub_department: str = None
