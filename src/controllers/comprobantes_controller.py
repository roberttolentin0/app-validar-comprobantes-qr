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


def list_tipo_comprobante() -> List[TipoComprobante]:
    return db_tipo_comprobante.list_all_type()


def get_comprobante_by_id(id) -> Comprobante:
    return db_comprobante.get_comprobante_by_id(id)


def get_comprobante_status_by_id(id) -> ViewComprobanteEstados:
    comprobante = db_comprobante.get_comprobante_with_status(id)
    return parsed_comprobante_with_status(comprobante)


def get_id_tipo_comprobante(cod_comprobante) -> int:
    tipos = db_tipo_comprobante.list_all_type()
    print(tipos)
    for tipo in tipos:
        if tipo.cod_comprobante == cod_comprobante:
            return tipo.id
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
def validar_en_sunat_individual(comprobante: Comprobante) -> dict:
    print('Validando...')
    estado_sunat = []
    data_comprobante = {
        "id": comprobante.id,
        "numRuc": comprobante.ruc,
        "codComp": "01", # Cambiar para que sea dinamico
        "numeroSerie": comprobante.serie,
        "numero": comprobante.numero,
        "fechaEmision": DateFormat.convert_date_to_ddmmyy(comprobante.fecha_emision), # "26/11/2023"
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
