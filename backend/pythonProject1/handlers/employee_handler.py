from fastapi import APIRouter, HTTPException
from db import get_employees_collection
from models import Employee

router = APIRouter()

# Эндпоинты для таблицы employees

@router.get("/employees", response_model=list[Employee])
def get_employees():
    conn, cur = get_employees_collection()
    cur.execute("SELECT * FROM employees;")
    employees = cur.fetchall()
    conn.close()
    return employees

@router.get("/employees/{employee_id}", response_model=Employee)
def get_employee(employee_id: int):
    conn, cur = get_employees_collection()
    cur.execute("SELECT * FROM employees WHERE id = %s;", (employee_id,))
    employee = cur.fetchone()
    conn.close()
    if employee:
        return employee
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

@router.post("/employees/", response_model=dict)
def create_employee(employee: Employee):
    conn, cur = get_employees_collection()
    sql = "INSERT INTO employees (name, role, email, phone, department) VALUES (%s, %s, %s, %s, %s);"
    values = (employee.name, employee.role, employee.email, employee.phone, employee.department)
    cur.execute(sql, values)
    conn.commit()
    conn.close()
    return {"message": "Employee created successfully"}

@router.put("/employees/{employee_id}", response_model=dict)
def update_employee(employee_id: int, employee: Employee):
    conn, cur = get_employees_collection()
    sql = "UPDATE employees SET name = %s, role = %s, email = %s, phone = %s, department = %s WHERE id = %s;"
    values = (employee.name, employee.role, employee.email, employee.phone, employee.department, employee_id)
    cur.execute(sql, values)
    conn.commit()
    conn.close()
    if cur.rowcount > 0:
        return {"message": "Employee updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

@router.delete("/employees/{employee_id}", response_model=dict)
def delete_employee(employee_id: int):
    conn, cur = get_employees_collection()
    cur.execute("DELETE FROM employees WHERE id = %s;", (employee_id,))
    conn.commit()
    conn.close()
    if cur.rowcount > 0:
        return {"message": "Employee deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Employee not found")
