from flask import Flask
from flask_cors import CORS
from backend.app.routes.tasks import tasks_bp
from backend.app.config import Config
from backend.app.models.tasks import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db()
    CORS(app)

    app.register_blueprint(tasks_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)