from flask import Blueprint, request, jsonify, redirect, url_for

from ..controllers import comprobantes_controller
from ..models.comprobanteModel import Comprobante

api_scope = Blueprint("api", __name__)

@api_scope.route('/comprobantes', methods=['GET'])
def get_list():
    comprobantes_list = comprobantes_controller.lists()
    comprobantes_dict = [comprobante.to_json() for comprobante in comprobantes_list]
    print(comprobantes_list)
    return jsonify(comprobantes_dict)

@api_scope.route('/comprobante', methods=['POST'])
def create():
    print('Crear permiso', request.form)
    if request.method == 'POST':
        # ruc = request.form['ruc']
        # fecha_emision = request.form['fecha_emision']
        # print('ruc_form', ruc)
        # serie = request.form['serie']
        # numero = request.form['numero']
        # monto = request.form['monto']
        # id_tipo_comprobante = request.form['id_tipo_comprobante']
        # comprobante_dict = Comprobante(
        #     ruc=ruc,
        #     fecha_emision=fecha_emision,
        #     serie=serie, numero=numero,
        #     monto=monto,
        #     id_tipo_comprobante=id_tipo_comprobante)

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