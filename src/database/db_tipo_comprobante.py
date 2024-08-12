from typing import List
from .db_connection import DBConnection
from ..models.tipoComprobanteModel import TipoComprobante

connection = DBConnection()

def list_all_type() -> List[TipoComprobante]:
    # print('Entro list all type')
    query = """
        SELECT id, cod_comprobante, descripcion
	    FROM public.tipo_comprobante;
    """
    records = connection._fetch_all(query=query)

    tipo_comprobantes = []
    for record in records:
        tipo = TipoComprobante(
                              id=record[0],
                              cod_comprobante=record[1],
                              descripcion=record[2])
        tipo_comprobantes.append(tipo)
    return tipo_comprobantes