import sqlite3
import json
from models import Employee


EMPLOYEES = [
]


def get_all_employees():
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        """)
        employees = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            employee = Employee(row['id'], row['name'],
                                row['address'],
                                row['location_id'])

            employees.append(employee.__dict__)
    return json.dumps(employees)


def get_single_employee(id):
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        WHERE e.id = ?
        """, (id, ))
        data = db_cursor.fetchone()
        employee = Employee(data['id'], data['name'],
                            data['address'],
                            data['location_id'])
        return json.dumps(employee.__dict__)


def create_employee(employee):
    max_id = EMPLOYEES[-1]["id"]
    new_id = max_id + 1
    employee["id"] = new_id
    EMPLOYEES.append(employee)
    return employee


def delete_employee(id):
    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM employee
        WHERE id = ?
        """, (id, ))


def update_employee(id, new_employee):
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            EMPLOYEES[index] = new_employee
            break
