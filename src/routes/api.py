import traceback
import re

from flask import Blueprint, request, jsonify, redirect, url_for

from ..controllers import comprobantes_controller
from ..models.comprobanteModel import Comprobante
from ..routes.errors import ComprobanteAlreadyExistsError, ComprobanteSunatError
from ..utils.DateFormat import DateFormat
from ..utils.Logger import Logger

api_scope = Blueprint("api", __name__)


@api_scope.route('/comprobantes', methods=['GET'])
def get_list():
    comprobantes_list = comprobantes_controller.lists()
    comprobantes_dict = [comprobante.to_json()
                         for comprobante in comprobantes_list]
    print(comprobantes_list)
    return jsonify(comprobantes_dict)


@api_scope.route('/create_comprobante', methods=['POST'])
def create_comprobante_qr():
    data = request.form
    print('Crear permiso QR', data)
    try:
        if request.method == 'POST':
            data_qr = data.get('dataQr', None)
            if data_qr is not None:
                # Para separaciones por '|' y ']'
                parsed_data_qr = re.split(r'\||\]', data_qr)
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
            else:
                data_comprobante = {
                    'ruc': data['ruc'],
                    'id_tipo_comprobante': comprobantes_controller.get_id_tipo_comprobante(data['tipoComprobante']),
                    'serie': data['serie'],
                    'numero': data['numero'],
                    'monto': data['monto'],
                    'fecha_emision': data['fechaEmision']
                }

            print('data_comprobante', data_comprobante)
            comprobante = Comprobante(
                ruc=data_comprobante['ruc'],
                fecha_emision=data_comprobante['fecha_emision'],
                serie=data_comprobante['serie'],
                numero=data_comprobante['numero'],
                monto=data_comprobante['monto'],
                id_tipo_comprobante=data_comprobante['id_tipo_comprobante'])
            # Create
            new_comprobante = comprobantes_controller.create(comprobante)
            comprobante_with_status = comprobantes_controller.get_comprobante_status_by_id(
                new_comprobante.id)
            print('new_comprobante', comprobante_with_status)
            return jsonify({'message': 'success', 'new_comprobante': comprobante_with_status.to_json()}), 200
    except ComprobanteAlreadyExistsError as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': f"Error: {e}"}), 500
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': f'Error al crear el comprobante: {e}'}), 500


@api_scope.route('/validar/comprobantes', methods=['POST'])
def validar_comprobantes():
    try:
        if request.method == 'POST':
            print('Validando...')
            estados_sunat = comprobantes_controller.validar_en_sunat()
            if not estados_sunat:
                return jsonify({'message': "No hay comprobantes a validar"}), 404
            return jsonify({'message': 'success', 'data': estados_sunat}), 200
    except ComprobanteSunatError as e:
        return jsonify({'message': f"Verificar comprobantes '{e}'"}), 500
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': f"Error en validar comprobantes: {e}"}), 500


@api_scope.route('/validar/comprobante', methods=['GET', 'POST'])
def validar_comprobante():
    try:
        if request.method == 'POST':
            data = request.json
            print('data', data)
            id = data['id']
            comprobante = comprobantes_controller.get_comprobante_by_id(id)
            print('Validando...')
            estado_sunat = comprobantes_controller.validar_en_sunat_individual(
                comprobante)
            print('Validado individualmente: ', estado_sunat)
            if not estado_sunat:
                return jsonify({'message': "Comprobante no validado"}), 404
            return jsonify({'message': 'success', 'data': estado_sunat}), 200
    except ComprobanteSunatError as e:
        return jsonify({'message': f"Verificar comprobante '{e}'"}), 500
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Error en validar comprobante"}), 500
