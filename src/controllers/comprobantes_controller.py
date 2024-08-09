from typing import List

from ..database import db_comprobante
from ..database import db_tipo_comprobante
from ..database import db_estado_comprobante
from ..models.comprobanteModel import Comprobante
from ..models.tipoComprobanteModel import TipoComprobante
from ..models.estadoComprobanteModel import EstadoComprobante
from ..models.viewComprobantesEstadosModel import ViewComprobanteEstados
from ..routes.errors import ComprobanteAlreadyExistsError
from ..services.validar_comprobante_sunat import validar_comprobante
from ..utils.helpers import parsed_comprobante_with_status
from ..utils.helpers import parse_qr_code
from ..utils.DateFormat import DateFormat
from ..utils.utils import measure_time


def create(comprobante_: Comprobante) -> Comprobante:
    '''Crear comprobante si no existe'''
    # Verificar si ya existe el comprobante
    comprobante = db_comprobante.get_comprobante(comprobante_)
    if comprobante:
        raise ComprobanteAlreadyExistsError(comprobante)
    return db_comprobante.create(comprobante_)


def delete_comprobante(comprobante_: Comprobante) -> Comprobante:
    return db_comprobante.delete(comprobante_)


def lists() -> List[Comprobante]:
    return db_comprobante.list_all()


def list_with_status() -> List[ViewComprobanteEstados]:
    comprobantes_estados = db_comprobante.list_all_with_status()
    for comprobante in comprobantes_estados:
        comprobante = parsed_comprobante_with_status(comprobante)
    return comprobantes_estados

def list_with_status_today() -> List[ViewComprobanteEstados]:
    comprobantes_estados = db_comprobante.list_all_with_status_today()
    for comprobante in comprobantes_estados:
        comprobante = parsed_comprobante_with_status(comprobante)
    return comprobantes_estados

def list_tipo_comprobante() -> List[TipoComprobante]:
    return db_tipo_comprobante.list_all_type()


def get_comprobante_by_id(id) -> Comprobante:
    return db_comprobante.get_comprobante_by_id(id)


def get_comprobante_status_by_id(id) -> ViewComprobanteEstados:
    comprobante = db_comprobante.get_comprobante_with_status(id)
    return parsed_comprobante_with_status(comprobante)


def get_tipo_comprobante(id=None, cod_comprobante=None) -> TipoComprobante:
    tipos = db_tipo_comprobante.list_all_type()
    for tipo in tipos:
        if tipo.id == id or tipo.cod_comprobante == cod_comprobante:
            return tipo
    return None


@measure_time
def validar_en_sunat() -> list:
    estados_sunat = []
    comprobantes_sin_estado = db_comprobante.list_statusless_comprobante()
    # print('comprobantes_sin_estado', comprobantes_sin_estado)
    if comprobantes_sin_estado is None:
        raise Exception('No hay comprobantes sin estado')
    for comprobante in comprobantes_sin_estado:
        estado_sunat = validar_en_sunat_individual(comprobante)
        estados_sunat.append(estado_sunat)
        # Validar comprobantes con la API Sunat
    print(f'-- Comprobantes validados: {len(estados_sunat)}/{len(comprobantes_sin_estado)}', estados_sunat)
    return estados_sunat

@measure_time
def validar_en_sunat_comprobantes_del_dia() -> list:
    estados_sunat = []
    comprobantes_sin_estado = db_comprobante.list_statusless_comprobante_del_dia()
    print('comprobantes_sin_estado_del_dia', comprobantes_sin_estado, len(comprobantes_sin_estado))
    if comprobantes_sin_estado is None:
        raise Exception('No hay comprobantes sin estado')

    for comprobante in comprobantes_sin_estado:
        estado_sunat = validar_en_sunat_individual(comprobante)
        estados_sunat.append(estado_sunat)
        # Validar comprobantes con la API Sunat
    print(f'-- Comprobantes del dia validados: {len(estados_sunat)}/{len(comprobantes_sin_estado)}', estados_sunat)
    return estados_sunat

@measure_time
def validar_en_sunat_individual(comprobante: Comprobante) -> dict:
    print('Validando...')
    print(comprobante)
    estado_sunat = []
    _fecha_emision = DateFormat.convert_str_to_date(comprobante.fecha_emision)
    data_comprobante = {
        "id": comprobante.id,
        "numRuc": comprobante.ruc,
        "codComp":  get_tipo_comprobante(id=comprobante.id_tipo_comprobante).cod_comprobante, # "01"
        "numeroSerie": comprobante.serie,
        "numero": comprobante.numero,
        "fechaEmision": DateFormat.convert_date_to_ddmmyy(_fecha_emision), # "26/11/2023"
        "monto": comprobante.monto  # "22725.00"
    }
    estado_sunat = validar_comprobante(data_comprobante)
    if estado_sunat is not None:
        observaciones = estado_sunat.get('observaciones', None)
        if observaciones is not None and len(observaciones) > 0:
            observaciones = ' '.join(estado_sunat['observaciones'])

        new_estado_comprobante = EstadoComprobante(
            id_comprobante=estado_sunat['id'],
            estado_comprobante=estado_sunat.get('estadoCp', None),
            estado_ruc=estado_sunat.get('estadoRuc', None),
            cod_domiciliaria_ruc=estado_sunat.get('condDomiRuc', None),
            observaciones=observaciones
        )
        print('Estado comprobante: ', new_estado_comprobante)
        estado_comprobante = db_estado_comprobante.get_estado_comprobante_by_id(comprobante.id)
        if estado_comprobante is None:
            db_estado_comprobante.create(new_estado_comprobante)
        else:
            db_estado_comprobante.update(new_estado_comprobante)
    return estado_sunat

def get_data_comprobante(data_form: dict, data_qr: str = None):
    '''
        param: data_form: diccionario con datos del formulario
        param: data_qr: string con el código QR (opcional)
        return: data_comprobante: diccionario con los datos del comprobante
    '''

    def parse_data(parsed_data):
        id_tipo_comprobante = get_tipo_comprobante(cod_comprobante=parsed_data[1].strip()).id
        fecha_emision = DateFormat.find_and_format_date(data=parsed_data[6]) if data_qr else parsed_data[6]

        return {
            'ruc': parsed_data[0].strip(),
            'id_tipo_comprobante': id_tipo_comprobante,
            'serie': parsed_data[2].strip(),
            'numero': parsed_data[3].strip(),
            'monto': parsed_data[5].strip(),
            'fecha_emision': fecha_emision
        }

    if data_qr:
        parsed_data_qr = parse_qr_code(data_qr)
        data_comprobante = parse_data(parsed_data_qr)
    else:
        parsed_data_form = [
            data_form['ruc'],
            data_form['tipoComprobante'],
            data_form['serie'],
            data_form['numero'],
            '',  # Placeholder para monto que se toma después
            data_form['monto'],
            data_form['fechaEmision']
        ]
        data_comprobante = parse_data(parsed_data_form)

    return data_comprobante