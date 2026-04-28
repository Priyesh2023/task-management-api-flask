# Task Management API

A production-like mini system built using **Flask, JWT Authentication, SQLite, and Swagger UI**.

---

## 🚀 Features

- User Registration & Login
- JWT Authentication
- Role Based Access (Admin/User)
- CRUD Operations for Tasks
- Assign Tasks to Users
- Admin can update any task
- User can update only assigned task
- Pagination
- Filtering by Status
- Swagger API Documentation
- Unit Testing with Pytest

---

## 🛠 Tech Stack

- Python
- Flask
- Flask-JWT-Extended
- Flask-SQLAlchemy
- SQLite
- Flasgger
- Pytest

---

## 📦 Installation

```bash
git clone https://github.com/Priyesh2023/task-management-api-flask.git
cd task-management-api-flask
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

# <<<<<<< HEAD

Run Project

Open in browser:

http://127.0.0.1:5000/

Swagger UI:

http://127.0.0.1:5000/apidocs/

## 🔐 1. Register Admin

POST /register

```json
{
  "username": "admin",
  "password": "123",
  "role": "admin"
}

2. Register User

POST /register

{
  "username": "priyesh",
  "password": "123",
  "role": "user"
}

3. Login Admin

POST /login

{
  "username": "admin",
  "password": "123"
}

POST /login

{
  "username": "priyesh",
  "password": "123"
}

5. Create Task (Admin)

POST /tasks

{
  "title": "Final Project",
  "description": "Complete before deadline",
  "status": "pending"
}

6. Get All Tasks

GET /tasks

(No body required)

7. Assign Task to User (Admin)

POST /assign/{task_id}/{user_id}

Example:

task_id = 2
user_id = 2


8. Update Task (User Assigned Task)

PUT /tasks/{id}

Example:

id = 2
{
  "title": "Final Project",
  "description": "Task Completed",
  "status": "completed"
}


9. Update Task (Admin)

PUT /tasks/{id}

{
  "title": "Updated Task",
  "description": "Updated by Admin",
  "status": "completed"
}


10. Delete Task (Admin Only)

DELETE /tasks/{id}

Example:

id = 2

11. Project Flow
Register Admin
Register User
Login Admin
Create Task
Get Tasks
Assign Task
Login User
Update Assigned Task
Login Admin
Delete Task

