class TipoComprobante():
    def __init__(
            self,
            id,
            cod_comprobante,
            descripcion) -> None:
        self.id=id
        self.cod_comprobante=cod_comprobante,
        self.descripcion=descripcion

    def to_json(self):
        return {
            'id': self.id,
            'cod_comprobante': self.cod_comprobante,
            'descripcion': self.descripcion
        }