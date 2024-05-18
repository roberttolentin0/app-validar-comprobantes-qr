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

def list_all_type() -> List[EstadoComprobante]:
    print('Entro list all status')
    query = """
        SELECT id, cod_comprobante, descripcion
	    FROM public.tipo_comprobante;
    """
    records = connection._fetch_all(query=query)

    tipo_comprobantes = []
    for record in records:
        tipo = EstadoComprobante(
                              id=record[0],
                              cod_comprobante=record[1],
                              descripcion=record[2])
        tipo_comprobantes.append(tipo)
    return tipo_comprobantes