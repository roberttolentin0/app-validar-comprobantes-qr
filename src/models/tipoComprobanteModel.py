from dataclasses import dataclass

@dataclass
class TipoComprobante():
    id: int
    cod_comprobante: str
    descripcion: str

    def to_json(self):
        return {
            'id': self.id,
            'cod_comprobante': self.cod_comprobante,
            'descripcion': self.descripcion
        }