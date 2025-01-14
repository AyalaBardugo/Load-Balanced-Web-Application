"""Main application entry point"""
from flask import Flask
from routes import RouteManager
import logging
from config import LogConfig

def create_app() -> Flask:
    """Initialize and configure Flask application
    Returns:
        Flask: Configured Flask application instance
    """
    LogConfig.setup_logging()
    app = Flask(__name__)
    RouteManager(app)
    logging.debug("Application started successfully")
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)