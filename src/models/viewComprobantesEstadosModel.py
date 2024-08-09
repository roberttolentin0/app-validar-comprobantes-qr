from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ViewComprobanteEstados:
    id: int
    ruc: str
    fecha_emision: str
    serie: str
    numero: int
    monto: float
    tipo_comprobante: str
    estado_comprobante: str
    estado_ruc: str
    cod_domiciliaria_ruc: str
    observaciones: str
    id_tipo_comprobante: Optional[int] = None
    created_at: Optional[datetime] = None

    def to_json(self):
        return {
            'id': self.id,
            'ruc': self.ruc,
            'fecha_emision': self.fecha_emision,
            'serie': self.serie,
            'numero': self.numero,
            'monto': self.monto,
            'tipo_comprobante': self.tipo_comprobante,
            'estado_comprobante': self.estado_comprobante,
            'estado_ruc': self.estado_ruc,
            'cod_domiciliaria_ruc': self.cod_domiciliaria_ruc,
            'observaciones': self.observaciones,
            'created_at': self.created_at
        }
