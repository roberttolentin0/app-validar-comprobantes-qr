from typing import List
from .db_connection import DBConnection
from ..models.estadoComprobanteModel import EstadoComprobante
from ..utils.DateFormat import DateFormat

connection = DBConnection()


def create(estado_comprobante: EstadoComprobante) -> EstadoComprobante:
    print('Entro create EstadoComprobante')
    # Definir la consulta con parámetros con nombres
    query = """
        INSERT INTO public.estado_comprobante
        (estado_comprobante, estado_ruc, cod_domiciliaria_ruc, observaciones, created_at, id_comprobante)
        VALUES (
        %(estado_comprobante)s,
        %(estado_ruc)s,
        %(cod_domiciliaria_ruc)s,
        %(observaciones)s,
        %(created_at)s,
        %(id_comprobante)s)
        RETURNING id
    """
    estado_dict = estado_comprobante.to_json()
    estado_dict['created_at'] = DateFormat.get_curr_time_peru()
    print('estado_dict', estado_dict)

    id_ = connection._fetch_lastrow_id(query, estado_dict)

    estado_dict["id"] = id_
    return EstadoComprobante(**estado_dict)


def update(estado_comprobante: EstadoComprobante) -> EstadoComprobante:
    print('--- Update estado', estado_comprobante)
    query = """
        UPDATE public.estado_comprobante
	    SET estado_comprobante=%(estado_comprobante)s, estado_ruc=%(estado_ruc)s, cod_domiciliaria_ruc=%(cod_domiciliaria_ruc)s, observaciones=%(observaciones)s, updated_at=%(updated_at)s
	    WHERE id_comprobante = %(id_comprobante)s
        RETURNING id
    """
    estado_dict = estado_comprobante.to_json()
    estado_dict['updated_at'] = DateFormat.get_curr_time_peru()
    id_ = connection._fetch_lastrow_id(query, estado_dict)
    print('id_ update', id_)
    return EstadoComprobante(**estado_dict)


def get_estado_comprobante_by_id(_id) -> EstadoComprobante:
    print('Entro get estado by id', _id)
    query = """
        SELECT id, estado_comprobante, estado_ruc, cod_domiciliaria_ruc, observaciones, updated_at, created_at, id_comprobante
	    FROM public.estado_comprobante WHERE id_comprobante = %(id_comprobante)s;
    """
    record = connection._fetch_one(
        query=query, parameters={'id_comprobante': _id})

    if record is not None:
        return EstadoComprobante(id=record[0],
                                 estado_comprobante=record[1],
                                 estado_ruc=record[2],
                                 cod_domiciliaria_ruc=record[3],
                                 observaciones=record[4],
                                 id_comprobante=record[7])
    return None
