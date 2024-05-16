from dataclasses import dataclass

@dataclass
class EstadoComprobante():
    id: int
    estado_comprobante: str
    estado_ruc: str
    cod_domiciliaria_ruc: str
    observaciones: str
    id_comprobante: int

    def to_json(self):
        return {
            'id': self.id,
            'estado_comprobante': self.estado_comprobante,
            'estado_ruc': self.estado_ruc,
            'cod_domiciliaria_ruc': self.cod_domiciliaria_ruc,
            'observaciones': self.observaciones,
            'id_comprobante': self.id_comprobante
        }