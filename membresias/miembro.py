# Clase Miembro
class Miembro:
	def __init__(self, id_miembro: str, nombre: str, correo: str, telefono: str):
		self._id_miembro = id_miembro
		self._nombre = nombre
		self._correo = correo
		self._telefono = telefono

	@property
	def id_miembro(self):
		return self._id_miembro.upper() 

	@id_miembro.setter
	def id_miembro(self, valor):
		if not valor:
			raise ValueError("El ID de miembro no puede estar vacío.")
		self._id_miembro = valor

	@property
	def nombre(self):
		return self._nombre

	@nombre.setter
	def nombre(self, valor):
		if not valor:
			raise ValueError("El nombre no puede estar vacío.")
		self._nombre = valor

	@property
	def correo(self):
		return self._correo

	@correo.setter
	def correo(self, valor):
		if not valor or '@' not in valor:
			raise ValueError("El correo debe ser válido.")
		self._correo = valor

	@property
	def telefono(self):
		return self._telefono

	@telefono.setter
	def telefono(self, valor):
		if not valor:
			raise ValueError("El teléfono no puede estar vacío.")
		self._telefono = valor

	def __str__(self):
		return f"{self.id_miembro} - {self.nombre} | {self.correo} | {self.telefono}"