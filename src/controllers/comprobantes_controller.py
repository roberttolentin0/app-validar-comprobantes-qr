from typing import List

from ..constans import CONDICION_DOMICILIO_CONTRIBUYENTE
from ..constans import ESTADO_COMPROBANTE
from ..constans import ESTADO_CONTRIBUYENTE
from ..database import db_comprobante
from ..database import db_tipo_comprobante
from ..models.comprobanteModel import Comprobante
from ..models.tipoComprobanteModel import TipoComprobante
from ..models.viewComprobantesEstadosModel import ViewComprobanteEstados
from ..routes.errors import ComprobanteAlreadyExistsError
from ..services.validar_comprobante_sunat import validar_comprobante
from ..utils.DateFormat import DateFormat

def create(comprobante_: Comprobante) -> Comprobante:
    '''Crear comprobante si no existe'''
    # Verificar si ya existe el comprobante
    comprobante = db_comprobante.get_comprobante(comprobante_)
    if comprobante:
        raise ComprobanteAlreadyExistsError(comprobante)
    return db_comprobante.create(comprobante_)

def lists() -> List[Comprobante]:
    return db_comprobante.list_all()

def list_with_status() -> List[ViewComprobanteEstados]:
    comprobantes_estados = db_comprobante.list_all_with_status()
    for comprobante in comprobantes_estados:
        # Mapea el estado del comprobante
        comprobante.estado_comprobante = ESTADO_COMPROBANTE.get(str(comprobante.estado_comprobante), '')
        # Mapea el estado del RUC
        comprobante.estado_ruc = ESTADO_CONTRIBUYENTE.get(str(comprobante.estado_ruc), '')
        # Mapea la condición de domicilio del contribuyente
        comprobante.cod_domiciliaria_ruc = CONDICION_DOMICILIO_CONTRIBUYENTE.get(str(comprobante.cod_domiciliaria_ruc), '')

    return comprobantes_estados

def list_tipo_comprobante() -> List[TipoComprobante]:
    return db_tipo_comprobante.list_all_type()

def get_id_tipo_comprobante(cod_comprobante) -> int:
    tipos = db_tipo_comprobante.list_all_type()
    print(tipos)
    for tipo in tipos:
        if tipo.cod_comprobante == cod_comprobante:
            return tipo.id
    return None

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
            "fechaEmision": DateFormat.convert_date_to_ddmmyy(comprobante.fecha_emision), # "26/11/2023"
            "monto": comprobante.monto # "22725.00"
        }
        estado_sunat = validar_comprobante(data_comprobante)
        estados_sunat.append(estado_sunat)
        # Validar comprobantes con la API Sunat
    print('-- Comprobantes validados: ', len(comprobantes_sin_estado), estados_sunat, len(estados_sunat))
    return estados_sunat