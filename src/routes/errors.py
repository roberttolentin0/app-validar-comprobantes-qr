class ComprobanteAlreadyExistsError(Exception):
    '''Excepción lanzada cuando el comprobante ya existe.'''
    def __init__(self, comprobante):
        self.comprobante = comprobante
        super().__init__(f"El comprobante {comprobante.serie}-{comprobante.numero} ya existe, con ID {comprobante.id}.")