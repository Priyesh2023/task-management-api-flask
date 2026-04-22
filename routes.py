from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Task


def register_routes(app):

    # Home
    @app.route("/")
    def home():
        return jsonify({"message": "Task Management API Running"})


    # Register User / Admin
    @app.route("/register", methods=["POST"])
    def register():
        data = request.get_json()

        role = data.get("role", "user")

        user = User(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            role=role
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "message": f"{role} registered successfully"
        }), 201


    # Login
    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()

        user = User.query.filter_by(email=data["email"]).first()

        if not user or user.password != data["password"]:
            return jsonify({"message": "Invalid credentials"}), 401

        token = create_access_token(identity=str(user.id))

        return jsonify({
            "token": token,
            "role": user.role
        }), 200


    # Create Task
    @app.route("/tasks", methods=["POST"])
    @jwt_required()
    def create_task():
        data = request.get_json()
        current_user = int(get_jwt_identity())

        task = Task(
            title=data["title"],
            description=data["description"],
            user_id=current_user
        )

        db.session.add(task)
        db.session.commit()

        return jsonify({
            "message": "Task created successfully"
        }), 201


    # Get Tasks (Pagination + Filtering)
    @app.route("/tasks", methods=["GET"])
    @jwt_required()
    def get_tasks():
        current_user = int(get_jwt_identity())

        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 5, type=int)
        status = request.args.get("status")

        query = Task.query.filter_by(user_id=current_user)

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
                "user_id": task.user_id
            })

        return jsonify({
            "page": page,
            "limit": limit,
            "total_tasks": tasks.total,
            "tasks": result
        }), 200


    # Update Task
    @app.route("/tasks/<int:id>", methods=["PUT"])
    @jwt_required()
    def update_task(id):
        task = Task.query.get(id)

        if not task:
            return jsonify({"message": "Task not found"}), 404

        data = request.get_json()

        task.title = data.get("title", task.title)
        task.description = data.get("description", task.description)
        task.status = data.get("status", task.status)

        db.session.commit()

        return jsonify({
            "message": "Task updated successfully"
        }), 200


    # Delete Task
    @app.route("/tasks/<int:id>", methods=["DELETE"])
    @jwt_required()
    def delete_task(id):
        task = Task.query.get(id)

        if not task:
            return jsonify({"message": "Task not found"}), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({
            "message": "Task deleted successfully"
        }), 200


    # Assign Task (Admin Only)
    @app.route("/tasks/<int:id>/assign", methods=["PUT"])
    @jwt_required()
    def assign_task(id):
        current_user = int(get_jwt_identity())
        user = User.query.get(current_user)

        if user.role != "admin":
            return jsonify({"message": "Admins only"}), 403

        task = Task.query.get(id)

        if not task:
            return jsonify({"message": "Task not found"}), 404

        data = request.get_json()
        task.user_id = data["user_id"]

        db.session.commit()

        return jsonify({
            "message": "Task assigned successfully"
        }), 200