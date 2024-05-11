from flask import Blueprint, render_template
from ..controllers import comprobantes_controller
from ..utils.DateFormat import DateFormat

global_scope = Blueprint("views", __name__)

nav = [
    {"name": "Listar Todos", "url": "/api/comprobantes"}
]


@global_scope.route("/", methods=['GET'])
def home():
    """Landing page route."""
    print('Homeee')
    comprobantes_list = comprobantes_controller.list_with_status()
    for comprobante in comprobantes_list:
        comprobante.fecha_emision = DateFormat.convert_date_to_ddmmyy(comprobante.fecha_emision)

    comprobantes_dict = [comprobante.to_json() for comprobante in comprobantes_list]
    print(comprobantes_list)
    parameters = {
        "title": "Validación de comprobantes con SUNAT",
        "description": "Vista con todos los comprobantes a validar",
        "comprobantes": comprobantes_dict
    }

    return render_template("home.html", nav=nav, **parameters)
