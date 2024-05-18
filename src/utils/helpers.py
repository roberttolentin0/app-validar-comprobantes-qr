from ..constans import CONDICION_DOMICILIO_CONTRIBUYENTE
from ..constans import ESTADO_COMPROBANTE
from ..constans import ESTADO_CONTRIBUYENTE
from ..models.viewComprobantesEstadosModel import ViewComprobanteEstados
from .DateFormat import DateFormat

def parsed_comprobante_with_status(_comprobante: ViewComprobanteEstados) -> ViewComprobanteEstados:
    # Mapea el estado del comprobante
    _comprobante.estado_comprobante = ESTADO_COMPROBANTE.get(str(_comprobante.estado_comprobante), '')
    # Mapea el estado del RUC
    _comprobante.estado_ruc = ESTADO_CONTRIBUYENTE.get(str(_comprobante.estado_ruc), '')
    # Mapea la condición de domicilio del contribuyente
    _comprobante.cod_domiciliaria_ruc = CONDICION_DOMICILIO_CONTRIBUYENTE.get(str(_comprobante.cod_domiciliaria_ruc), '')
    _comprobante.fecha_emision = DateFormat.convert_date_to_ddmmyy(_comprobante.fecha_emision)
    return _comprobante