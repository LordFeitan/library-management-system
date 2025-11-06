import re
from datetime import datetime

# Nueva validación para el ID del libro
def validar_id_libro(id_libro):
	if not id_libro or not isinstance(id_libro, str):
		raise ValueError('El ID debe ser un texto no vacío.')
	if len(id_libro) < 3:
		raise ValueError('El ID debe tener al menos 3 caracteres.')
	if not id_libro.isalnum():
		raise ValueError('El ID solo puede contener caracteres alfanuméricos (sin espacios ni símbolos).')

def validar_titulo(titulo):
	"""
	Valida el título del libro.
	Permite letras, números, espacios, acentos y signos de puntuación comunes.
	"""
	if not titulo or not isinstance(titulo, str):
		raise ValueError('El título debe ser un texto no vacío.')
	
	titulo = titulo.strip()
	
	if len(titulo) < 1:
		raise ValueError('El título no puede estar vacío.')
	
	if len(titulo) > 200:
		raise ValueError('El título no puede exceder 200 caracteres.')
	
	# Permite letras, números, espacios, acentos y signos de puntuación comunes en títulos
	patron = r'^[a-zA-Z0-9áéíóúüñÁÉÍÓÚÜÑ\s.,;:()\-\'\"!?]+$'
	if not re.match(patron, titulo):
		raise ValueError('El título contiene caracteres no permitidos. Use solo letras, números, espacios y puntuación básica.')

def validar_anio(anio):
	"""
	Valida que el año sea un número entero dentro de un rango razonable.
	"""
	if not isinstance(anio, int):
		raise ValueError('El año debe ser un número entero.')
	
	anio_actual = datetime.now().year
	
	if anio < 1000:
		raise ValueError('El año debe ser mayor o igual a 1000.')
	
	if anio > anio_actual + 1:
		raise ValueError(f'El año no puede ser mayor a {anio_actual + 1}.')

def validar_autor(autor):
	"""
	Valida que el autor tenga nombre y nacionalidad válidos.
	"""
	if not autor or not hasattr(autor, 'nombre'):
		raise ValueError('El autor debe ser válido y tener un nombre.')
	
	nombre = autor.nombre.strip()
	
	if len(nombre) < 2:
		raise ValueError('El nombre del autor debe tener al menos 2 caracteres.')
	
	if len(nombre) > 100:
		raise ValueError('El nombre del autor no puede exceder 100 caracteres.')
	
	# Validar que el nombre del autor solo contenga letras, espacios y acentos
	patron = r'^[a-záéíóúüñA-ZÁÉÍÓÚÜÑ\s.]+$'
	if not re.match(patron, nombre):
		raise ValueError('El nombre del autor solo puede contener letras, espacios, acentos y puntos.')
	
	# Validar nacionalidad si existe
	if hasattr(autor, 'nacionalidad') and autor.nacionalidad:
		nacionalidad = autor.nacionalidad.strip()
		if len(nacionalidad) > 50:
			raise ValueError('La nacionalidad no puede exceder 50 caracteres.')
		
		patron_nac = r'^[a-záéíóúüñA-ZÁÉÍÓÚÜÑ\s]+$'
		if not re.match(patron_nac, nacionalidad):
			raise ValueError('La nacionalidad solo puede contener letras, espacios y acentos.')

def validar_categoria(categoria_id):
	"""
	Valida que el ID de categoría exista en el catálogo de categorías.
	"""
	if not categoria_id:
		raise ValueError('La categoría no puede estar vacía.')
	
	# Si es un objeto con atributo 'nombre', convertir a string
	if hasattr(categoria_id, 'nombre'):
		categoria_id = str(categoria_id.nombre)
	else:
		categoria_id = str(categoria_id)
	
	categoria_id = categoria_id.strip()
	
	# Validar formato de ID (CATXXX)
	if not categoria_id.startswith('CAT'):
		raise ValueError('El ID de categoría debe comenzar con "CAT".')
	
	if len(categoria_id) != 6:
		raise ValueError('El ID de categoría debe tener el formato CATXXX (ej: CAT001).')
	
	# Verificar que exista en categorias.json
	from datos.json_manager import cargar_datos
	categorias = cargar_datos('datos/categorias.json')
	
	if not any(cat['id_categoria'] == categoria_id for cat in categorias):
		raise ValueError(f'El ID de categoría "{categoria_id}" no existe en el catálogo.')
