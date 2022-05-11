"""Initialize Flask app."""
from flask import Flask
from flask_assets import Environment, Bundle

def init_app() -> Flask:
    """Construct core Flask application with possible Dash app."""
    fapp = Flask(__name__, instance_relative_config=False)
    fapp.config.from_object('config.Config')

    with fapp.app_context():
        # Import parts of our core Flask app
        from . import routes

        # # Import Dash application
        # from .dashapp import init_dashboard
        # fapp = init_dashboard(fapp)

        return fapp