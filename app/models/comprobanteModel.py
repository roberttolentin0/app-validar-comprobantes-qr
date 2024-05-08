from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Comprobante:
    ruc: str
    fecha_emision: str
    serie: str
    numero: int
    monto: float
    id_tipo_comprobante: Optional[int] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_json(self):
        return {
            'id': self.id,
            'ruc': self.ruc,
            'fecha_emision': self.fecha_emision,
            'serie': self.serie,
            'numero': self.numero,
            'monto': self.monto,
            'id_tipo_comprobante': self.id_tipo_comprobante,
            'created_at': self.created_at
        }
