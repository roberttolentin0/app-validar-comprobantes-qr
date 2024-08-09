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
    comprobantes_list = comprobantes_controller.list_with_status_today()
    comprobantes_dict = [comprobante.to_json() for comprobante in comprobantes_list]
    # print(comprobantes_list)
    parameters = {
        "title": "Validación de comprobantes con SUNAT",
        "description": "Vista con todos los comprobantes a validar",
        "comprobantes": comprobantes_dict,
        "show_validar_comprobantes_hoy": True
    }

    return render_template("home.html", nav=nav, **parameters)

@global_scope.route("/lista_comprobantes", methods=['GET'])
def lista_comprobantes():
    """Lista comprobantes route."""
    print('All comprobantes')
    comprobantes_list = comprobantes_controller.list_with_status()
    comprobantes_dict = [comprobante.to_json() for comprobante in comprobantes_list]
    # print(comprobantes_list)
    parameters = {
        "title": "Historial de comprobantes validados en SUNAT",
        "description": "Vista con todos los comprobantes registrados",
        "comprobantes": comprobantes_dict,
        "show_validar_masivo": True
    }

    return render_template("list_comprobantes.html", nav=nav, **parameters)