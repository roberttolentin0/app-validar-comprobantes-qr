from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class EstadoComprobante():
    id_comprobante: int
    estado_comprobante: Optional[str] = None
    estado_ruc: Optional[str] = None
    cod_domiciliaria_ruc: Optional[str] = None
    observaciones: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_json(self):
        return {
            'id': self.id,
            'estado_comprobante': self.estado_comprobante,
            'estado_ruc': self.estado_ruc,
            'cod_domiciliaria_ruc': self.cod_domiciliaria_ruc,
            'observaciones': self.observaciones,
            'id_comprobante': self.id_comprobante
        }
