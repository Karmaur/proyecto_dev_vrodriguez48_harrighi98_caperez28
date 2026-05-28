class ClienteDestino:
    def __init__(self, nombre, apellido, pais, telefono, correo_electronico):
        self.nombre = nombre
        self.apellido = apellido
        self.pais = pais
        self.telefono = telefono
        self.correo = correo_electronico

    def mostrar_info(self):
        return (
            f"{self.nombre} {self.apellido} - "
            f"{self.correo} - "
            f"Tel: {self.telefono}"
        )
