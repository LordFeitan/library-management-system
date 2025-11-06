

# Nueva validación para el ID del libro
def validar_id_libro(id_libro):
	if not id_libro or not isinstance(id_libro, str):
		raise ValueError('El ID debe ser un texto no vacío.')
	if len(id_libro) < 3:
		raise ValueError('El ID debe tener al menos 3 caracteres.')
	if not id_libro.isalnum():
		raise ValueError('El ID solo puede contener caracteres alfanuméricos (sin espacios ni símbolos).')

def validar_titulo(titulo):
	if not titulo or not isinstance(titulo, str):
		raise ValueError('El título debe ser un texto no vacío.')
	# Permitir solo títulos alfanuméricos y espacios
	if not all(c.isalnum() or c.isspace() for c in titulo):
		raise ValueError('El título solo puede contener caracteres alfanuméricos y espacios.')

def validar_anio(anio):
	if not isinstance(anio, int) or anio < 0:
		raise ValueError('El año debe ser un número entero positivo.')

def validar_autor(autor):
	if not autor or not hasattr(autor, 'nombre'):
		raise ValueError('El autor debe ser válido.')

def validar_categoria(categoria):
	if not categoria or not hasattr(categoria, 'nombre'):
		raise ValueError('La categoría debe ser válida.')
