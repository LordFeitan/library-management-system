# Clase Categoria

class Categoria:
	def __init__(self, nombre: str, descripcion: str = ""):
		self._nombre = nombre
		self._descripcion = descripcion

	@property
	def nombre(self):
		return self._nombre

	@nombre.setter
	def nombre(self, valor):
		if not valor:
			raise ValueError("El nombre de la categoría no puede estar vacío.")
		self._nombre = valor

	@property
	def descripcion(self):
		return self._descripcion

	@descripcion.setter
	def descripcion(self, valor):
		self._descripcion = valor

	def __str__(self):
		return f"{self.nombre}: {self.descripcion}"