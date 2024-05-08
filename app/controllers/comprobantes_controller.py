from typing import List

from ..database import db_comprobante
from ..models.comprobanteModel import Comprobante
from ..helpers import helper
from ..services.validar_comprobante_sunat import validar_comprobante


def create(comprobante_: Comprobante) -> Comprobante:
    # comprobante = helper.format_name(comprobante_)
    # helper.validate_comprobante(comprobante)
    return db_comprobante.create(comprobante_)


def lists() -> List[Comprobante]:
    return db_comprobante.list_all()


def validar_en_sunat() -> list:
    estados_sunat = []
    comprobantes_sin_estado = db_comprobante.list_statusless_comprobante()
    print('comprobantes_sin_estado', comprobantes_sin_estado)
    for comprobante in comprobantes_sin_estado:
        print(comprobante.ruc)
        data_comprobante = {
            "id": comprobante.id,
            "numRuc": comprobante.ruc,
            "codComp": "01",
            "numeroSerie": comprobante.serie,
            "numero": comprobante.numero,
            "fechaEmision": "26/11/2023", # comprobante.fecha_emision,
            "monto": comprobante.monto
        }
        # data_comprobante = {
        #         "numRuc": "20522199495",
        #         "codComp": "01",
        #         "numeroSerie": "F001",
        #         "numero": "55285",
        #         "fechaEmision": "30/11/2023",
        #         "monto": "22725.00"
        # }

        estado_sunat = validar_comprobante(data_comprobante)
        estados_sunat.append(estado_sunat)
        # Validar comprobantes con la API Sunat
    print('comprobantes_por_validar', len(comprobantes_sin_estado), estados_sunat, len(estados_sunat))
    return estados_sunat