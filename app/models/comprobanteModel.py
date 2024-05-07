from dataclasses import dataclass

@dataclass
class Comprobante:
    id: int
    ruc: str
    fecha_emision: str
    serie: str
    numero: int
    monto: float
    id_tipo_comprobante: int

    def to_json(self):
        return {
            'id': self.id,
            'ruc': self.ruc,
            'fecha_emision': self.fecha_emision,
            'serie': self.serie,
            'numero': self.numero,
            'monto': self.monto,
            'id_tipo_comprobante': self.id_tipo_comprobante
        }
