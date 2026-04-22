# Task Management API

A Flask-based Task Management API developed to demonstrate backend development concepts such as authentication, task management, role-based access control, pagination, filtering, and testing.

---

## Features

- User Registration and Login
- JWT Authentication
- Create, Read, Update, Delete Tasks
- Assign Tasks to Users
- Role-Based Access Control (Admin/User)
- Pagination Support
- Status Filtering
- SQLite Database Integration
- Unit Testing with Pytest

---

## Tech Stack

- Python
- Flask
- Flask-JWT-Extended
- Flask-SQLAlchemy
- SQLite
- Pytest

---

## Project Structure

task-management-api/
│── app.py  
│── config.py  
│── models.py  
│── routes.py  
│── database.db  
│── requirements.txt  
│── README.md  
│── tests/  
│ └── test_app.py

---

## Installation and Run

```bash
git clone <your-repository-link>
cd task-management-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```