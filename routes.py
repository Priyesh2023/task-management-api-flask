from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Task


def register_routes(app):

    # -------------------------
    # Helper: Check Admin Role
    # -------------------------
    def is_admin():
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        return user and user.role == "admin"

    # -------------------------
    # Register User
    # -------------------------
    @app.route('/register', methods=['POST'])
    def register():
        """
        Register User
        ---
        tags:
          - Auth
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - username
                - password
              properties:
                username:
                  type: string
                password:
                  type: string
                role:
                  type: string
                  example: admin
        responses:
          200:
            description: User Registered
        """
        data = request.get_json()

        if not data:
            return jsonify({"msg": "No input data"}), 400

        username = data.get("username")
        password = data.get("password")
        role = data.get("role", "user")

        if not username or not password:
            return jsonify({"msg": "Username and password required"}), 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"msg": "User already exists"}), 400

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            password=hashed_password,
            role=role
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({"msg": "User Registered"})

    # -------------------------
    # Login
    # -------------------------
    @app.route('/login', methods=['POST'])
    def login():
        """
        Login User
        ---
        tags:
          - Auth
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - username
                - password
              properties:
                username:
                  type: string
                password:
                  type: string
        responses:
          200:
            description: JWT Token
        """
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            token = create_access_token(identity=str(user.id))
            return jsonify(access_token=token)

        return jsonify({"msg": "Invalid credentials"}), 401

    # -------------------------
    # Get Tasks
    # -------------------------
    @app.route('/tasks', methods=['GET'])
    @jwt_required()
    def get_tasks():
        """
        Get Tasks
        ---
        tags:
          - Tasks
        security:
          - Bearer: []
        parameters:
          - name: page
            in: query
            type: integer
          - name: limit
            in: query
            type: integer
          - name: status
            in: query
            type: string
        responses:
          200:
            description: Task List
        """
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        status = request.args.get("status")

        query = Task.query

        # Normal user sees only assigned tasks
        if user.role != "admin":
            query = query.filter_by(assigned_to=user.id)

        if status:
            query = query.filter_by(status=status)

        tasks = query.paginate(page=page, per_page=limit, error_out=False)

        result = []
        for task in tasks.items:
            result.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "assigned_to": task.assigned_to
            })

        return jsonify(result)

    # -------------------------
    # Create Task (Admin Only)
    # -------------------------
    @app.route('/tasks', methods=['POST'])
    @jwt_required()
    def create_task():
        """
        Create Task
        ---
        tags:
          - Tasks
        security:
          - Bearer: []
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - title
              properties:
                title:
                  type: string
                description:
                  type: string
        responses:
          200:
            description: Task Created
        """
        if not is_admin():
            return jsonify({"msg": "Admin only"}), 403

        data = request.get_json()

        task = Task(
            title=data.get("title"),
            description=data.get("description")
        )

        db.session.add(task)
        db.session.commit()

        return jsonify({"msg": "Task Created"})

    # -------------------------
    # Update Task
    # Admin = any task
    # User = only assigned task
    # -------------------------
    @app.route('/tasks/<int:id>', methods=['PUT'])
    @jwt_required()
    def update_task(id):
        """
        Update Task
        ---
        tags:
          - Tasks
        security:
          - Bearer: []
        parameters:
          - name: id
            in: path
            type: integer
            required: true
          - in: body
            name: body
            schema:
              type: object
              properties:
                title:
                  type: string
                description:
                  type: string
                status:
                  type: string
        responses:
          200:
            description: Task Updated
        """
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        task = Task.query.get_or_404(id)

        # Admin sab update karega
        # User sirf assigned task update karega
        if user.role != "admin" and task.assigned_to != user.id:
            return jsonify({"msg": "Not allowed"}), 403

        data = request.get_json()

        task.title = data.get("title", task.title)
        task.description = data.get("description", task.description)
        task.status = data.get("status", task.status)

        db.session.commit()

        return jsonify({"msg": "Task Updated"})

    # -------------------------
    # Delete Task (Admin Only)
    # -------------------------
    @app.route('/tasks/<int:id>', methods=['DELETE'])
    @jwt_required()
    def delete_task(id):
        """
        Delete Task
        ---
        tags:
          - Tasks
        security:
          - Bearer: []
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Task Deleted
        """
        if not is_admin():
            return jsonify({"msg": "Admin only"}), 403

        task = Task.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()

        return jsonify({"msg": "Task Deleted"})

    # -------------------------
    # Assign Task (Admin Only)
    # -------------------------
    @app.route('/assign/<int:task_id>/<int:user_id>', methods=['POST'])
    @jwt_required()
    def assign_task(task_id, user_id):
        """
        Assign Task
        ---
        tags:
          - Tasks
        security:
          - Bearer: []
        parameters:
          - name: task_id
            in: path
            type: integer
            required: true
          - name: user_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Task Assigned
        """
        if not is_admin():
            return jsonify({"msg": "Admin only"}), 403

        task = Task.query.get_or_404(task_id)
        user = User.query.get_or_404(user_id)

        task.assigned_to = user.id
        db.session.commit()

        return jsonify({"msg": "Task Assigned"})