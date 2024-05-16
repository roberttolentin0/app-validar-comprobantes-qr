from flask import Flask
from config import Config

# from .routes import global_scope, api_scope # Con esto no hace falta saber los archivos que hay en routes
# Routes
from .routes.routes import global_scope
from .routes.api import api_scope

# Crear aplicación de flask
app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATE_FOLDER)

def init_app():
    print('INIT APPPP')
    app.config.from_object(Config)

    # Registrar vistas | Blueprints
    app.register_blueprint(global_scope, url_prefix="/")
    # app.register_blueprint(errors_scope, url_prefix="/")
    app.register_blueprint(api_scope, url_prefix="/api")
    return app
