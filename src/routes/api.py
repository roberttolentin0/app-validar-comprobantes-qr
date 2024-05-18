import re
from flask import Blueprint, request, jsonify, redirect, url_for

from ..controllers import comprobantes_controller
from ..models.comprobanteModel import Comprobante
from ..routes.errors import ComprobanteAlreadyExistsError
from ..utils.DateFormat import DateFormat

api_scope = Blueprint("api", __name__)

@api_scope.route('/comprobantes', methods=['GET'])
def get_list():
    comprobantes_list = comprobantes_controller.lists()
    comprobantes_dict = [comprobante.to_json() for comprobante in comprobantes_list]
    print(comprobantes_list)
    return jsonify(comprobantes_dict)

@api_scope.route('/create_comprobante', methods=['POST'])
def create_comprobante_qr():
    data = request.form
    print('Crear permiso QR', data)
    try:
        if request.method == 'POST':
            data_qr = request.form['dataQr']
            if data_qr is not None:
                parsed_data_qr = re.split(r'\||\]', data_qr) # Para separaciones por '|' y ']'
                print('parse_data_qr', parsed_data_qr)
                fecha = DateFormat.find_and_format_date(data=data_qr)
                data_comprobante = {
                    'ruc': parsed_data_qr[0],
                    'id_tipo_comprobante': comprobantes_controller.get_id_tipo_comprobante(parsed_data_qr[1]),
                    'serie': parsed_data_qr[2],
                    'numero': parsed_data_qr[3],
                    'monto': parsed_data_qr[5],
                    'fecha_emision': fecha
                }

                comprobante = Comprobante(
                    ruc=data_comprobante['ruc'],
                    fecha_emision=data_comprobante['fecha_emision'],
                    serie=data_comprobante['serie'],
                    numero=data_comprobante['numero'],
                    monto=data_comprobante['monto'],
                    id_tipo_comprobante=data_comprobante['id_tipo_comprobante'])
                # Create
                new_comprobante = comprobantes_controller.create(comprobante)
                comprobante_with_status = comprobantes_controller.get_comprobante_status_by_id(new_comprobante.id)
                print('new_comprobante', comprobante_with_status)
                return jsonify({'message': 'success', 'new_comprobante': comprobante_with_status.to_json()}), 200
    except ComprobanteAlreadyExistsError as e:
        return jsonify({'message': f"Error: {e}"}), 500
    except Exception as e:
        print(e)
        return jsonify({'message': "Error al crear el comprobante"}), 500

@api_scope.route('/comprobante', methods=['POST'])
def create_comprobante():
    print('Crear permiso', request.form)
    if request.method == 'POST':
        comprobante = Comprobante(
            ruc="20522199495",
            fecha_emision="30/11/2023",
            serie="F001", numero="55285",
            monto="22725.00",
            id_tipo_comprobante=1)
        # Create
        new_comprobante = comprobantes_controller.create(comprobante)
        print('new_comprobante', new_comprobante)
        return jsonify({'message': 'success', 'new_id': new_comprobante.id}), 200

    # if affected_rows == 1:
    #     return jsonify({'message': 'success', 'data': {'dni': permission.dni}}), 200
    # else:
    #     return jsonify({'message': "Error on insert"}), 500

@api_scope.route('/validar/comprobantes', methods=['POST'])
def validar_comprobantes():
    try:
        if request.method == 'POST':
            print('Validando...')
            estados_sunat = comprobantes_controller.validar_en_sunat()
            print('estados_sunat', estados_sunat)
            if not estados_sunat:
                return jsonify({'message': "No hay comprobantes a validar"}), 404
            return jsonify({'message': 'success', 'data': estados_sunat}), 200
    except Exception as e:
        return jsonify({'message': "Error en validar comprobante"}), 500