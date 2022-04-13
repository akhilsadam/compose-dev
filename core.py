"""Initialize Flask app."""
from flask import Flask
from flask_assets import Environment, Bundle
import sys
import app.options

ipa = sys.argv[1]
app.options.options.sethost(ipa)

def init_app():
    """Construct core Flask application with possible Dash app."""
    fapp = Flask(__name__, instance_relative_config=False)
    fapp.config.from_object('config.Config')

    with fapp.app_context():
        import app.api.data

        return fapp

"""Application entry point."""
if __name__ == "__main__":
    app = init_app()
    port = 5026
    app.run(host="0.0.0.0", debug=False,port=port)