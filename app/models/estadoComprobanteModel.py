class EstadoComprobante():
    def __init__(
            self,
            id,
            estado_comprobante,
            estado_ruc,
            cod_domiciliaria_ruc,
            observaciones,
            id_comprobante) -> None:
        self.id=id
        self.estado_comprobante=estado_comprobante
        self.estado_ruc=estado_ruc
        self.cod_domiciliaria_ruc=cod_domiciliaria_ruc
        self.observaciones=observaciones
        self.id_comprobante=id_comprobante

    def to_json(self):
        return {
            'id': self.id,
            'estado_comprobante': self.estado_comprobante,
            'estado_ruc': self.estado_ruc,
            'cod_domiciliaria_ruc': self.cod_domiciliaria_ruc,
            'observaciones': self.observaciones,
            'id_comprobante': self.id_comprobante
        }