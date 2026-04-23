# Task Management API

A production-like mini system built using Flask, JWT Authentication, SQLite, and Swagger.

## Features

- User Registration & Login
- JWT Authentication
- Role Based Access (Admin/User)
- CRUD Operations for Tasks
- Assign Tasks to Users
- Pagination
- Filtering
- Swagger API Docs
- Unit Testing with Pytest

## Tech Stack

- Python
- Flask
- Flask-JWT-Extended
- SQLAlchemy
- SQLite
- Flasgger
- Pytest

## Installation

```bash
git clone <your-repo-link>
cd task-management-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py