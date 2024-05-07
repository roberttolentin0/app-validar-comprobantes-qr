from typing import List

from ..database import comprobante_db
from ..models.comprobanteModel import Comprobante
from ..helpers import helper


def create(comprobante_: Comprobante) -> Comprobante:
    # comprobante = helper.format_name(comprobante_)
    # helper.validate_comprobante(comprobante)
    return comprobante_db.create(comprobante_)


def lists() -> List[Comprobante]:
    return comprobante_db.list_all()