import re

def validar_id_miembro(id_miembro):
	if not id_miembro or not isinstance(id_miembro, str):
		raise ValueError('El ID de miembro debe ser un texto no vacío.')

def validar_nombre(nombre):
	"""
	Valida que el nombre contenga solo letras (incluyendo acentos y ñ) y espacios.
	"""
	if not nombre or not isinstance(nombre, str):
		raise ValueError('El nombre debe ser un texto no vacío.')
	
	nombre = nombre.strip()
	
	if len(nombre) < 2:
		raise ValueError('El nombre debe tener al menos 2 caracteres.')
	
	if len(nombre) > 100:
		raise ValueError('El nombre no puede exceder 100 caracteres.')
	
	# Permite letras (a-z, A-Z), espacios, acentos y ñ
	patron = r'^[a-záéíóúüñA-ZÁÉÍÓÚÜÑ\s]+$'
	if not re.match(patron, nombre):
		raise ValueError('El nombre solo puede contener letras, espacios y acentos. No se permiten números ni caracteres especiales.')

def validar_correo(correo):
	"""
	Valida que el correo tenga un formato válido usando expresión regular.
	Formato básico: usuario@dominio.extension
	"""
	if not correo or not isinstance(correo, str):
		raise ValueError('El correo debe ser un texto no vacío.')
	
	correo = correo.strip()
	
	# Expresión regular para validar email
	# Permite: letras, números, puntos, guiones y guiones bajos antes del @
	# Requiere @ y un dominio válido con extensión
	patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
	
	if not re.match(patron, correo):
		raise ValueError('El correo no tiene un formato válido. Ejemplo válido: usuario@dominio.com')
	
	if len(correo) > 254:  # RFC 5321
		raise ValueError('El correo es demasiado largo (máximo 254 caracteres).')

def validar_telefono(telefono):
	"""
	Valida que el teléfono contenga solo dígitos y tenga una longitud razonable.
	Acepta teléfonos de 7 a 15 dígitos (estándares internacionales).
	"""
	if not telefono or not isinstance(telefono, str):
		raise ValueError('El teléfono debe ser un texto no vacío.')
	
	# Limpiar espacios, guiones y paréntesis para validación
	telefono_limpio = telefono.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
	
	if not telefono_limpio.isdigit():
		raise ValueError('El teléfono solo puede contener números (se permiten espacios y guiones como separadores).')
	
	if len(telefono_limpio) < 7:
		raise ValueError('El teléfono debe tener al menos 7 dígitos.')
	
	if len(telefono_limpio) > 15:
		raise ValueError('El teléfono no puede tener más de 15 dígitos.')
