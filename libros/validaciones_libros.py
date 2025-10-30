
def validar_isbn(isbn):
	if not isbn or not isinstance(isbn, str):
		raise ValueError('El ISBN debe ser un texto no vacío.')
	if len(isbn) < 5:
		raise ValueError('El ISBN debe tener al menos 5 caracteres.')

def validar_titulo(titulo):
	if not titulo or not isinstance(titulo, str):
		raise ValueError('El título debe ser un texto no vacío.')

def validar_anio(anio):
	if not isinstance(anio, int) or anio < 0:
		raise ValueError('El año debe ser un número entero positivo.')

def validar_autor(autor):
	if not autor or not hasattr(autor, 'nombre'):
		raise ValueError('El autor debe ser válido.')

def validar_categoria(categoria):
	if not categoria or not hasattr(categoria, 'nombre'):
		raise ValueError('La categoría debe ser válida.')
