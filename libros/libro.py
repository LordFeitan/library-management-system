# Clase Libro

from .autor import Autor
from .categoria import Categoria

class Libro:
	def __init__(self, id_libro: str, titulo: str, autor: Autor, categoria: str, anio: int, disponible: bool = True):
		self._id = id_libro
		self._titulo = titulo
		self._autor = autor
		self._categoria = categoria
		self._anio = anio
		self._disponible = disponible


	@property
	def id(self):
		return self._id

	@id.setter
	def id(self, valor):
		if not valor:
			raise ValueError("El ID no puede estar vacío.")
		self._id = valor

	@property
	def titulo(self):
		return self._titulo

	@titulo.setter
	def titulo(self, valor):
		if not valor:
			raise ValueError("El título no puede estar vacío.")
		self._titulo = valor

	@property
	def autor(self):
		return self._autor

	@autor.setter
	def autor(self, valor):
		if not isinstance(valor, Autor):
			raise ValueError("El autor debe ser una instancia de Autor.")
		self._autor = valor

	@property
	def categoria(self):
		return self._categoria

	@categoria.setter
	def categoria(self, valor):
		if not isinstance(valor, str):
			raise ValueError("La categoría debe ser un string.")
		self._categoria = valor

	@property
	def anio(self):
		return self._anio

	@anio.setter
	def anio(self, valor):
		if not isinstance(valor, int) or valor < 0:
			raise ValueError("El año debe ser un número entero positivo.")
		self._anio = valor

	@property
	def disponible(self):
		return self._disponible

	@disponible.setter
	def disponible(self, valor):
		if not isinstance(valor, bool):
			raise ValueError("El estado de disponibilidad debe ser booleano.")
		self._disponible = valor

	def __str__(self):
		return f"[{self.id}] {self.titulo} - {self.autor} | {self.categoria} | Año: {self.anio} | {'Disponible' if self.disponible else 'Prestado'}"