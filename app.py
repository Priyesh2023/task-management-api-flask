from flask import Flask
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from models import db
from config import Config
from routes import register_routes

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)
Swagger(app)

@app.route("/")
def home():
    return {"msg": "Task Management API Running Successfully"}

with app.app_context():
    db.create_all()

register_routes(app)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)