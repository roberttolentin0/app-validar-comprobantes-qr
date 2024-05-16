TIPO_COMPROBANTE = {
    "01": "FACTURA",
    "03": "BOLETA DE VENTA",
    "04": "LIQUIDACIÓN DE COMPRA",
    "07": "NOTA DE CREDITO",
    "08": "NOTA DE DEBITO",
    "R1": "RECIBO POR HONORARIOS",
    "R7": "NOTA DE CREDITO DE RECIBOS",
}

ESTADO_COMPROBANTE = {
    "0": "NO EXISTE", # Comprobante no informado
    "1": "ACEPTADO",  # Comprobante aceptado
    "2": "ANULADO",  # Comunicado en una baja
    "3": "AUTORIZADO",  # Con autorización de imprenta
    "4": "NO AUTORIZADO"  # No autorizado por imprenta
}

ESTADO_CONTRIBUYENTE = {
    "00" : "ACTIVO",
    "01" : "BAJA PROVISIONAL",
    "02" : "BAJA PROV. POR OFICIO",
    "03" : "SUSPENSION TEMPORAL",
    "10" : "BAJA DEFINITIVA",
    "11" : "BAJA DE OFICIO",
    "22" : "INHABILITADO-VENT.UNICA",
}

CONDICION_DOMICILIO_CONTRIBUYENTE = {
    "00" : "HABIDO",
    "09" : "PENDIENTE",
    "11" : "POR VERIFICAR",
    "12" : "NO HABIDO",
    "20" : "NO HALLADO",
}