import re
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


def convert_to_postgres_format(amount_str):
    # Eliminar comas que están seguidas de tres dígitos (separadores de miles)
    amount_str = re.sub(r'(?<=\d),(?=\d{3}\b)', '', amount_str)
    # Reemplazar la coma decimal por un punto decimal
    amount_str = amount_str.replace(',', '.')
    return amount_str


def parse_qr_code(input_str):
    # Separar la entrada usando el delimitador común '|'
    parts = re.split(r'\||\]', input_str)
    # Eliminar cualquier parte vacía al final
    parts = [part for part in parts if part]

    # Identificar si hay una parte que contiene un guion (serie-número combinados)
    if len(parts) > 3 and '-' in parts[2]:
        series, number = parts[2].split('-')
        parts = parts[:2] + [series, number] + parts[3:]
    elif len(parts) > 4 and re.match(r'^[A-Za-z0-9]+$', parts[2]) and re.match(r'^\d+$', parts[3]):
        series = parts[2]
        number = parts[3]
        parts = parts[:2] + [series, number] + parts[4:]

    # Convertir las cantidades si están en el formato incorrecto
    if len(parts) > 4:
        parts[4] = convert_to_postgres_format(parts[4])
    if len(parts) > 5:
        parts[5] = convert_to_postgres_format(parts[5])

    return parts