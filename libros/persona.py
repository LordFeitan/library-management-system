
class Persona:
    def __init__(self, nombre: str, nacionalidad: str = None):
        self._nombre = nombre
        self._nacionalidad = nacionalidad

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor:
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor

    @property
    def nacionalidad(self):
        return self._nacionalidad

    @nacionalidad.setter
    def nacionalidad(self, valor):
        self._nacionalidad = valor

    def descripcion(self):
        return f"{self.nombre} - {self.nacionalidad or 'N/A'}"
