from persona import Persona

class Autor(Persona):
    def __init__(self, nombre: str, nacionalidad: str):
        super().__init__(nombre, nacionalidad)  

    def __str__(self):
        return f"{self.nombre} ({self.nacionalidad})"
