from flask import Blueprint, render_template
from ..controllers import comprobantes_controller

global_scope = Blueprint("views", __name__)

nav = [
    {"name": "Listar Todos", "url": "/api/comprobantes"}
]


@global_scope.route("/", methods=['GET'])
def home():
    """Landing page route."""
    print('Homeee')
    comprobantes_list = comprobantes_controller.list_with_status()
    comprobantes_dict = [comprobante.to_json() for comprobante in comprobantes_list]
    print(comprobantes_list)
    parameters = {
        "title": "Lista de comprobantes",
        "description": "Vista con todos los comprobantes a validar",
        "data": comprobantes_dict
    }

    return render_template("home.html", nav=nav, **parameters)
