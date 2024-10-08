import re
from ..constans import CONDICION_DOMICILIO_CONTRIBUYENTE
from ..constans import ESTADO_COMPROBANTE
from ..constans import ESTADO_CONTRIBUYENTE
from ..constans import RUC_EMPRESA
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
    _comprobante.created_at = DateFormat.convert_date_to_ddmmyy(_comprobante.created_at)
    return _comprobante


def convert_to_postgres_format(amount_str):
    ''' Para los montos eliminar comas que están seguidas de tres dígitos (separadores de miles) '''
    amount_str = re.sub(r'(?<=\d),(?=\d{3}\b)', '', amount_str)
    # Reemplazar la coma decimal por un punto decimal
    amount_str = amount_str.replace(',', '.')
    return amount_str

# Función para extraer y convertir los valores
def parse_list_with_signs(lista_entrada):
    '''
        param: lista_entrada: lista de strings con los valores a transformar
            ex ['-fdig-index.php_vr¿20609834774', 'td¿01', 'nd¿0002780', 'vs¿F002', "fec¿2024'06'06", 'mon¿2301.67']
        return: lista de valores transformados
            ex ['20609834774', '01', 'F002', '0002780', '0', '2301.67', "2024'06'06"]
        caso de ejemplo:
            ROCADMG
    '''

    resultado = [None] * 7  # Inicializa la lista con None para las 7 posiciones
    for item in lista_entrada:
        clave, valor = item.split('¿')
        if clave == '-fdig-index.php_vr':
            resultado[0] = valor  # Convierte a entero y coloca en la posición 0
        elif clave == 'td':
            resultado[1] = valor  # Convierte a entero y coloca en la posición 1
        elif clave == 'nd':
            resultado[3] = valor  # Coloca en la posición 3
        elif clave == 'vs':
            resultado[2] = valor  # Coloca en la posición 2
        elif clave == 'fec':
            resultado[6] = valor  # Coloca en la posición 6
        elif clave == 'mon':
            valor = valor.replace("'", '') # Si '14.82
            resultado[5] = valor  # Coloca en la posición 5

    resultado[4] = 'No se muestra IGV'

    return resultado


def parse_qr_code(input_str: str) -> list:
    '''input_str: 20100127165|01|F100|00451161|99.61|653.06|2024-05-22|6|20609699982|hgH0bEf7HK57HHPG1p6ZihmbQvI='''
    # Separar la entrada usando el delimitador '|' or ']'
    parts = re.split(r'\||\]|\/', input_str)
    print(parts)

    # Transformar parts de tipo ['-fdig-index.php_vr¿20609834774', 'td¿01', 'nd¿0002780', 'vs¿F002', "fec¿2024'06'06", 'mon¿2301.67']
    if '¿' in parts[0]:
        parts = parse_list_with_signs(parts)
        print('parts sin ¿ : ', parts)

    # Transformar parts si el RUC de la empresa está en la posición 3
    # Ex [6, 20602289029, 6, 20609699982, 01, F010-00001387, 2023-03-08, 102.97, 675.00, Pb4eBPZCAYkGBCh6FLKivNpPKAE=]
    if len(parts) > 3 and parts[3] == RUC_EMPRESA:
        parts = [parts[1]] + parts[4:6] + parts[7:9] + [parts[6]]  # [20602289029, 01, F010-00001387, 2023-03-08, 102.97, 675.00, Pb4eBPZCAYkGBCh6FLKivNpPKAE=]

    # Transformar parts si el RUC del emisor tiene mas de 11 dígitos, obtener los 11 últimos dígitos
    # Ex ['}00002620601114934', '01', 'FF01', '00008041', '86.00', '563.75', "01'06'2024", '20609699982', 'TERRANOVA TRADING S.A.C.', '']
    if len(parts[0]) > 11:
        parts[0] = parts[0][-11:]

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
