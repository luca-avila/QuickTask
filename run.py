from flask import Flask, jsonify
from flask_cors import CORS
from backend.app.routes.tasks import tasks_bp
from backend.app.config import Config
from backend.app.models.tasks import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db()
    CORS(app)

    # Register error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad Request',
            'message': 'Invalid request data'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'error': 'Method Not Allowed',
            'message': 'The HTTP method is not allowed for this endpoint'
        }), 405

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500

    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'QuickTask API',
            'version': '1.0.0'
        }), 200

    # Root endpoint
    @app.route('/')
    def root():
        return jsonify({
            'message': 'QuickTask API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/health',
                'tasks': '/tasks',
                'documentation': 'See README.md for API documentation'
            }
        }), 200

    app.register_blueprint(tasks_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)