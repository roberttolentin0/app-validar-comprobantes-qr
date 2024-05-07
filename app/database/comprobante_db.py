import pytz
from datetime import datetime
from typing import List

from .db_connection import DBConnection
# from ..models.models import Contact
from ..models.comprobanteModel import Comprobante

connection = DBConnection()
peru_timezone = pytz.timezone('America/Lima')
def get_curr_time_peru():
    return datetime.now(peru_timezone)


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
    comprobante_dict['created_at'] = get_curr_time_peru()
    print('comprobante_dict', comprobante_dict)

    id_ = connection._fetch_lastrow_id(query, comprobante_dict)

    comprobante_dict["id"] = id_
    return Comprobante(**comprobante_dict)


def list_all() -> List[Comprobante]:
    print('Entro list all')
    query = "SELECT * FROM comprobantes"
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