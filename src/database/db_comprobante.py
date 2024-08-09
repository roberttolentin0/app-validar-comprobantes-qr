from typing import List

from .db_connection import DBConnection
from ..models.comprobanteModel import Comprobante
from ..models.viewComprobantesEstadosModel import ViewComprobanteEstados
from ..utils.DateFormat import DateFormat

connection = DBConnection()


def create(comprobante: Comprobante) -> Comprobante:
    print('Entro create comprobante')
    # Definir la consulta con parámetros con nombres
    query = """
        INSERT INTO comprobantes
        (ruc, fecha_emision, serie, numero, monto, created_at, id_tipo_comprobante)
        VALUES (
        %(ruc)s,
        %(fecha_emision)s,
        %(serie)s,
        %(numero)s,
        %(monto)s,
        %(created_at)s,
        %(id_tipo_comprobante)s)
        RETURNING id
    """
    comprobante_dict = comprobante.to_json()
    comprobante_dict['created_at'] = DateFormat.get_curr_time_peru()
    # print('comprobante_dict', comprobante_dict)
    id_ = connection._fetch_lastrow_id(query, comprobante_dict)

    comprobante_dict["id"] = id_
    return Comprobante(**comprobante_dict)


def delete(comprobante: Comprobante) -> Comprobante:
    query = """
        DELETE FROM public.comprobantes
        WHERE id = %(id)s
    """
    parameters = {'id': comprobante.id}
    connection._fetch_none(query, parameters)
    return comprobante


def get_comprobante_by_id(_id) -> Comprobante:
    ''' @params: id
        @return: comprobante '''
    query = """
        SELECT id, ruc, fecha_emision, serie, numero, monto, updated_at, created_at, id_tipo_comprobante
	    FROM public.comprobantes WHERE id = %(id)s
    """
    parameters = {'id': _id}

    record = connection._fetch_one(query=query, parameters=parameters)
    if record is not None:
        return Comprobante(id=record[0],
                        ruc=record[1],
                        fecha_emision=record[2],
                        serie=record[3],
                        numero=record[4],
                        monto=record[5],
                        id_tipo_comprobante=record[8],
                        created_at=record[7])
    return None

def get_comprobante(comprobante: Comprobante) -> Comprobante:
    ''' @params: ruc, serie, numero, monto
        @return: comprobante '''
    print('Obtener comprobante')
    query = """
        SELECT id, ruc, fecha_emision, serie, numero, monto, updated_at, created_at, id_tipo_comprobante
	    FROM public.comprobantes WHERE ruc = %(ruc)s AND serie = %(serie)s AND numero = %(numero)s AND monto = %(monto)s
    """
    parameters = {}
    parameters['ruc'] = comprobante.ruc
    parameters['serie'] = comprobante.serie
    parameters['numero'] = comprobante.numero
    parameters['monto'] = comprobante.monto
    record = connection._fetch_one(query=query, parameters=parameters)
    if record is not None:
        return Comprobante(id=record[0],
                        ruc=record[1],
                        fecha_emision=record[2],
                        serie=record[3],
                        numero=record[4],
                        monto=record[5],
                        id_tipo_comprobante=record[8],
                        created_at=record[7])
    return None

def list_all() -> List[Comprobante]:
    print('Entro list all')
    query = """
        SELECT id, ruc, fecha_emision, serie, numero, monto, updated_at, created_at, id_tipo_comprobante
	    FROM public.comprobantes
    """
    records = connection._fetch_all(query=query)

    comprobantes = []
    for record in records:
        comprobante = Comprobante(id=record[0],
                              ruc=record[1],
                              fecha_emision=record[2],
                              serie=record[3],
                              numero=record[4],
                              monto=record[5],
                              id_tipo_comprobante=record[8],
                              created_at=record[7])
        comprobantes.append(comprobante)
    return comprobantes

def get_comprobante_with_status(_id) -> ViewComprobanteEstados:
    print('Obtener comprobante')
    query = """
        SELECT id, ruc, fecha_emision, serie, numero, monto, tipo_comprobante, estado_comprobante, estado_ruc, cod_domiciliaria_ruc, observaciones
	    FROM public.view_comprobantes_con_estados WHERE id = %(id)s
    """
    parameters = {'id': _id}

    record = connection._fetch_one(query=query, parameters=parameters)
    if record is not None:
        return ViewComprobanteEstados(
                                id=record[0],
                                ruc=record[1],
                                fecha_emision=record[2],
                                serie=record[3],
                                numero=record[4],
                                monto=record[5],
                                tipo_comprobante=record[6],
                                estado_comprobante=record[7],
                                estado_ruc=record[8],
                                cod_domiciliaria_ruc=record[9],
                                observaciones=record[10])
    return None

def list_all_with_status() -> List[ViewComprobanteEstados]:
    print('Entro list all status')
    query = """
        SELECT id, ruc, fecha_emision, serie, numero, monto, tipo_comprobante, estado_comprobante, estado_ruc, cod_domiciliaria_ruc, observaciones, created_at
	    FROM public.view_comprobantes_con_estados;
    """
    records = connection._fetch_all(query=query)

    comprobantes = []
    for record in records:
        comprobante = ViewComprobanteEstados(
                                id=record[0],
                                ruc=record[1],
                                fecha_emision=record[2],
                                serie=record[3],
                                numero=record[4],
                                monto=record[5],
                                tipo_comprobante=record[6],
                                estado_comprobante=record[7],
                                estado_ruc=record[8],
                                cod_domiciliaria_ruc=record[9],
                                observaciones=record[10],
                                created_at=record[11])
        comprobantes.append(comprobante)
    return comprobantes

def list_all_with_status_today() -> List[ViewComprobanteEstados]:
    print('Get lista de comprobantes del dia')
    today = DateFormat.get_curr_time_peru()
    today = today.strftime("%Y-%m-%d")
    query = """
        SELECT
            id, ruc, fecha_emision, serie, numero, monto, tipo_comprobante, estado_comprobante, estado_ruc, cod_domiciliaria_ruc, observaciones, created_at
	    FROM public.view_comprobantes_con_estados
        WHERE created_at = %(created_at)s
        ORDER BY id DESC
        ;
    """
    parameters = {'created_at': today}
    records = connection._fetch_all(query=query, parameters=parameters)
    print('records', records)
    comprobantes = []
    for record in records:
        comprobante = ViewComprobanteEstados(
                                id=record[0],
                                ruc=record[1],
                                fecha_emision=record[2],
                                serie=record[3],
                                numero=record[4],
                                monto=record[5],
                                tipo_comprobante=record[6],
                                estado_comprobante=record[7],
                                estado_ruc=record[8],
                                cod_domiciliaria_ruc=record[9],
                                observaciones=record[10],
                                created_at=record[11])
        comprobantes.append(comprobante)
    return comprobantes

def list_statusless_comprobante() -> list[Comprobante]:
    query = """
        SELECT id, ruc, fecha_emision, serie, numero, monto, updated_at, created_at, id_tipo_comprobante
	    FROM public.view_comprobantes_sin_estados ORDER BY id DESC;
    """
    records = connection._fetch_all(query=query)

    comprobantes = []
    for record in records:
        comprobante = Comprobante(
                              id=record[0],
                              ruc=record[1],
                              fecha_emision=record[2],
                              serie=record[3],
                              numero=record[4],
                              monto=record[5],
                              created_at=record[7],
                              id_tipo_comprobante=record[8])
        comprobantes.append(comprobante)
    return comprobantes

def list_statusless_comprobante_del_dia() -> list[Comprobante]:
    today = DateFormat.get_curr_time_peru()
    today = today.strftime("%Y-%m-%d")
    query = """
        SELECT
            c.id,
            c.ruc,
            c.fecha_emision,
            c.serie,
            c.numero,
            c.monto,
            c.created_at,
            c.id_tipo_comprobante,
            ec.estado_comprobante
        FROM comprobantes c
        LEFT JOIN estado_comprobante ec ON c.id = ec.id_comprobante
        WHERE
            (ec.id_comprobante IS NULL
            OR ec.estado_comprobante IS NULL
            OR ec.estado_comprobante <> 1)
    AND c.created_at = %(created_at)s
    """
    parameters = {'created_at': today}
    records = connection._fetch_all(query=query, parameters=parameters)
    print('records', records)

    comprobantes = []
    for record in records:
        comprobante = Comprobante(
                              id=record[0],
                              ruc=record[1],
                              fecha_emision=record[2],
                              serie=record[3],
                              numero=record[4],
                              monto=record[5],
                              created_at=record[6],
                              id_tipo_comprobante=record[7])
        comprobantes.append(comprobante)
    return comprobantes