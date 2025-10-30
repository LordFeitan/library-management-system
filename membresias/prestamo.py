# Clase Prestamo
from libros.libro import Libro
from .miembro import Miembro
from datetime import date

class Prestamo:
	def __init__(self, id_prestamo: str, miembro: Miembro, libro: Libro, fecha_prestamo: date, fecha_devolucion: date = None):
		self._id_prestamo = id_prestamo
		self._miembro = miembro
		self._libro = libro
		self._fecha_prestamo = fecha_prestamo
		self._fecha_devolucion = fecha_devolucion

	@property
	def id_prestamo(self):
		return self._id_prestamo

	@property
	def miembro(self):
		return self._miembro

	@property
	def libro(self):
		return self._libro

	@property
	def fecha_prestamo(self):
		return self._fecha_prestamo

	@property
	def fecha_devolucion(self):
		return self._fecha_devolucion

	@fecha_devolucion.setter
	def fecha_devolucion(self, valor):
		self._fecha_devolucion = valor

	def __str__(self):
		return f"Préstamo {self.id_prestamo}: {self.libro.titulo} a {self.miembro.nombre} el {self.fecha_prestamo} {'(Devuelto)' if self.fecha_devolucion else '(Pendiente)'}"