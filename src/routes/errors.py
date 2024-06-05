class ComprobanteAlreadyExistsError(Exception):
    '''Excepción lanzada cuando el comprobante ya existe.'''
    def __init__(self, comprobante):
        self.comprobante = comprobante
        super().__init__(f"El comprobante {comprobante.serie}-{comprobante.numero} ya existe, con ID {comprobante.id}.")


class ComprobanteSunatError(Exception):
    '''Excepción para cuando hay un mensaje de error del comprobante al verificar con la API Sunat'''
    def __init__(self, message):
        self.message = message
        super().__init__(message)