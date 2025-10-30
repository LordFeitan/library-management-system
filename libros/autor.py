# Clase Autor

class Autor:
	def __init__(self, nombre: str, nacionalidad: str):
		self._nombre = nombre
		self._nacionalidad = nacionalidad

	@property
	def nombre(self):
		return self._nombre

	@nombre.setter
	def nombre(self, valor):
		if not valor:
			raise ValueError("El nombre del autor no puede estar vacío.")
		self._nombre = valor

	@property
	def nacionalidad(self):
		return self._nacionalidad

	@nacionalidad.setter
	def nacionalidad(self, valor):
		if not valor:
			raise ValueError("La nacionalidad no puede estar vacía.")
		self._nacionalidad = valor

	def __str__(self):
		return f"{self.nombre} ({self.nacionalidad})"