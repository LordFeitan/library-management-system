
def validar_id_miembro(id_miembro):
	if not id_miembro or not isinstance(id_miembro, str):
		raise ValueError('El ID de miembro debe ser un texto no vacío.')

def validar_nombre(nombre):
	if not nombre or not isinstance(nombre, str):
		raise ValueError('El nombre debe ser un texto no vacío.')

def validar_correo(correo):
	if not correo or '@' not in correo:
		raise ValueError('El correo debe ser válido.')

def validar_telefono(telefono):
	if not telefono or not isinstance(telefono, str):
		raise ValueError('El teléfono debe ser un texto no vacío.')
