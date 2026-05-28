class ClienteRemitente:
    def __init__(self, nombre, apellido, pais, correo, documento, telefono,
                 direccion, ocupacion, origen_fondos):
        self.nombre = nombre
        self.apellido = apellido
        self.pais = pais
        self.correo = correo
        self.documento = documento
        self.telefono = telefono
        self.direccion = direccion
        self.ocupacion = ocupacion
        self.origen_fondos = origen_fondos

    def mostrar_info(self):
        return (
            f"{self.nombre} {self.apellido} - "
            f"{self.correo} - "
            f"Tel: {self.telefono}"
        )
