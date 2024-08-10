import traceback
import re

from flask import Blueprint, request, jsonify
from requests import ConnectionError

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
def create_comprobante():
    try:
        if request.method == 'POST':
            data = request.form
            data_qr = data.get('dataQr', None)
            print('Crear permiso: Data QR', data_qr)
            # if data_qr is not None:
            #     # Crear por DATA QR
            #     parsed_data_qr = parse_qr_code(data_qr)
            #     fecha = DateFormat.find_and_format_date(data=parsed_data_qr[6])
            #     id_tipo_comprobante = comprobantes_controller.get_tipo_comprobante(cod_comprobante=parsed_data_qr[1].strip()).id
            #     data_comprobante = {
            #         'ruc': parsed_data_qr[0].strip(),
            #         'id_tipo_comprobante': id_tipo_comprobante,
            #         'serie': parsed_data_qr[2].strip(),
            #         'numero': parsed_data_qr[3].strip(),
            #         'monto': parsed_data_qr[5].strip(),
            #         'fecha_emision': fecha
            #     }
            # else:
            #     # Crear Manualmente
            #     id_tipo_comprobante = comprobantes_controller.get_tipo_comprobante(cod_comprobante=data['tipoComprobante'].strip()).id
            #     data_comprobante = {
            #         'ruc': data['ruc'].strip(),
            #         'id_tipo_comprobante': id_tipo_comprobante,
            #         'serie': data['serie'].strip(),
            #         'numero': data['numero'].strip(),
            #         'monto': data['monto'].strip(),
            #         'fecha_emision': data['fechaEmision']
            #     }
            data_comprobante = comprobantes_controller.get_data_comprobante(data_form=data, data_qr=data_qr)
            print('data_comprobante', data_comprobante)
            # Verificar que todas las claves tengan valores
            for key, value in data_comprobante.items():
                if value is None or (isinstance(value, str) and not value.strip()):
                    raise ValueError(f"El valor para '{key}' no puede estar vacío o ser nulo.")

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
    except ValueError as e:
        return jsonify({'message': f"CÓDIGO QR INCORRECTO: {e}"}), 500
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': f'CÓDIGO QR INCORRECTO, INGRESE MANUALMENTE...  Detalle: {e}'}), 500


@api_scope.route('/create_and_validate', methods=['POST'])
def create_and_validate():
    try:
        if request.method == 'POST':
            data = request.form
            data_qr = data.get('dataQr', None)
            print('Crear permiso: Data QR', data_qr)
            data_comprobante = comprobantes_controller.get_data_comprobante(data_form=data, data_qr=data_qr)
            print('data_comprobante', data_comprobante)
            # Verificar que todas las claves tengan valores
            for key, value in data_comprobante.items():
                if value is None or (isinstance(value, str) and not value.strip()):
                    raise ValueError(f"El valor para '{key}' no puede estar vacío o ser nulo.")

            comprobante = Comprobante(
                ruc=data_comprobante['ruc'],
                fecha_emision=data_comprobante['fecha_emision'],
                serie=data_comprobante['serie'],
                numero=data_comprobante['numero'],
                monto=data_comprobante['monto'],
                id_tipo_comprobante=data_comprobante['id_tipo_comprobante'])
            # Create
            new_comprobante = comprobantes_controller.create(comprobante)
            msg = ''
            # Verificar en Sunat apenas se Scannea
            try:
                estado_sunat = comprobantes_controller.validar_en_sunat_individual(new_comprobante)
                # print('estado_sunat', estado_sunat)
                if not estado_sunat:
                    msg = msg + ', Pero no se pudo validar en SUNAT.'
            except Exception as e:
                Logger.add_to_log("error", str(e))
                msg = f'{msg}, Pero con errores al validar en SUNAT. {str(e)}'

            comprobante_with_status = comprobantes_controller.get_comprobante_status_by_id(
                new_comprobante.id)
            print('new_comprobante', comprobante_with_status)
            return jsonify({'message': msg, 'new_comprobante': comprobante_with_status.to_json()}), 200
    except ComprobanteAlreadyExistsError as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': f"Error: {e}"}), 500
    except ValueError as e:
        return jsonify({'message': f"CÓDIGO QR INCORRECTO: {e}"}), 500
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': f'CÓDIGO QR INCORRECTO, Ingrese manualmente...'}), 500


# Eliminar comprobante y estados
@api_scope.route('/delete_comprobante', methods=['POST'])
def delete_comprobante():
    try:
        if request.method == 'POST':
            data = request.json
            id = data['id']
            comprobante = comprobantes_controller.get_comprobante_by_id(id)
            comprobantes_controller.delete_comprobante(comprobante)
            return jsonify({'message': 'success'}), 200
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': f"Error al eliminar el comprobante: {e}"}), 500


@api_scope.route('/validar/comprobantes', methods=['POST'])
def validar_comprobantes():
    try:
        if request.method == 'POST':
            estados_sunat = comprobantes_controller.validar_en_sunat()
            if not estados_sunat:
                return jsonify({'message': "No hay comprobantes a validar"}), 404

        comprobantes_dict = get_comprobantes_with_status()
        return jsonify({'message': 'success', 'info': f'Se verifico {len(estados_sunat)}', 'data_comprobantes': comprobantes_dict}), 200
    except ComprobanteSunatError as e:
        return jsonify({'message': f"Verificar comprobantes '{e}'"}), 500
    except ConnectionError as e:
        return jsonify({'message': f"Verificar la Conexión a Internet"}), 500
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': f"Error en validar comprobantes: {e}"}), 500

@api_scope.route('/validar/comprobantes_del_dia', methods=['POST'])
def validar_comprobantes_del_dia():
    try:
        if request.method == 'POST':
            estados_sunat = comprobantes_controller.validar_en_sunat_comprobantes_del_dia()
            if not estados_sunat:
                return jsonify({'message': "No hay comprobantes a validar"}), 404

            comprobantes_dict = get_comprobantes_with_status_today()
            return jsonify({'message': 'success', 'info': f'Se verifico {len(estados_sunat)}', 'data_comprobantes': comprobantes_dict}), 200
    except ComprobanteSunatError as e:
        return jsonify({'message': f"Verificar comprobantes '{e}'"}), 500
    except ConnectionError as e:
        return jsonify({'message': f"Verificar la Conexión a Internet"}), 500
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': f"Error en validar comprobantes: {e}"}), 500

@api_scope.route('/validar/comprobante', methods=['GET', 'POST'])
def validar_comprobante():
    try:
        if request.method == 'POST':
            data = request.json
            id = data['id']
            comprobante = comprobantes_controller.get_comprobante_by_id(id)
            estado_sunat = comprobantes_controller.validar_en_sunat_individual(
                comprobante)
            comprobante_with_status = comprobantes_controller.get_comprobante_status_by_id(comprobante.id)
            print('Validado individualmente: ', estado_sunat)
            if not estado_sunat:
                return jsonify({'message': "Comprobante no validado"}), 404
            return jsonify({'message': 'success', 'data_comprobante': comprobante_with_status}), 200
    except ComprobanteSunatError as e:
        return jsonify({'message': f"Verificar comprobante '{e}'"}), 500
    except ConnectionError as e:
        return jsonify({'message': f"Verificar la conexión a Internet"}), 500
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': f"Error en validar comprobante '{e}'"}), 500


def get_comprobantes_with_status()-> dict:
    comprobantes_list = comprobantes_controller.list_with_status()
    return [comprobante.to_json() for comprobante in comprobantes_list]

def get_comprobantes_with_status_today()-> dict:
    comprobantes_list = comprobantes_controller.list_with_status_today()
    return [comprobante.to_json() for comprobante in comprobantes_list]