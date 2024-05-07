from flask import Blueprint, render_template

global_scope = Blueprint("views", __name__)

nav = [
    {"name": "Listar Todos", "url": "/api/comprobantes"}
]


@global_scope.route("/", methods=['GET'])
def home():
    """Landing page route."""
    print('Homeee')
    parameters = {
        "title": "Lista de comprobantes",
        "description": "Vista con todos los comprobantes a validar"
    }

    return render_template("home.html", nav=nav, **parameters)
