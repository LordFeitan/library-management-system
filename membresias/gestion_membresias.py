# Gestión de préstamos y miembros
from datos.json_manager import cargar_datos, guardar_datos
from .miembro import Miembro
from libros.gestion_libros import buscar_libro_por_id, modificar_libro
from .prestamo import Prestamo
from datetime import date

RUTA_JSON_PRESTAMOS = 'datos/prestamos.json'

def listar_prestamos():
	datos = cargar_datos(RUTA_JSON_PRESTAMOS)
	return datos

def registrar_prestamo(id_prestamo, id_miembro, id_libro):
	prestamos = cargar_datos(RUTA_JSON_PRESTAMOS)
	miembros = cargar_datos(RUTA_JSON_MIEMBROS)
	libro = buscar_libro_por_id(id_libro)
	if not libro:
		raise ValueError('Libro no encontrado.')
	if not libro.get('disponible', True):
		raise ValueError('El libro no está disponible.')
	miembro = next((m for m in miembros if m['id_miembro'] == id_miembro), None)
	if not miembro:
		raise ValueError('Miembro no encontrado.')
	if any(p['libro']['id'] == id_libro and not p.get('fecha_devolucion') for p in prestamos):
		raise ValueError('El libro ya está prestado.')
	prestamo = {
		'id_prestamo': id_prestamo,
		'miembro': miembro,
		'libro': libro,
		'fecha_prestamo': str(date.today()),
		'fecha_devolucion': None
	}
	prestamos.append(prestamo)
	# Marcar libro como no disponible
	modificar_libro(id_libro, {'disponible': False})
	guardar_datos(RUTA_JSON_PRESTAMOS, prestamos)

def devolver_prestamo(id_prestamo):
	prestamos = cargar_datos(RUTA_JSON_PRESTAMOS)
	for p in prestamos:
		if p['id_prestamo'] == id_prestamo and not p.get('fecha_devolucion'):
			p['fecha_devolucion'] = str(date.today())
			# Marcar libro como disponible
			id_libro = p['libro']['id']
			modificar_libro(id_libro, {'disponible': True})
			guardar_datos(RUTA_JSON_PRESTAMOS, prestamos)
			return
	raise ValueError('Préstamo no encontrado o ya devuelto.')

RUTA_JSON_MIEMBROS = 'datos/miembros.json'

def listar_miembros():
	datos = cargar_datos(RUTA_JSON_MIEMBROS)
	return [Miembro(m['id_miembro'], m['nombre'], m['correo'], m['telefono']) for m in datos]

def buscar_miembro_por_id(id_miembro):
	miembros = cargar_datos(RUTA_JSON_MIEMBROS)
	for m in miembros:
		if m['id_miembro'] == id_miembro:
			return m
	return None

def agregar_miembro(miembro: Miembro):
	miembros = cargar_datos(RUTA_JSON_MIEMBROS)
	if any(m['id_miembro'] == miembro.id_miembro for m in miembros):
		raise ValueError('Ya existe un miembro con ese ID.')
	miembros.append({
		'id_miembro': miembro.id_miembro,
		'nombre': miembro.nombre,
		'correo': miembro.correo,
		'telefono': miembro.telefono
	})
	guardar_datos(RUTA_JSON_MIEMBROS, miembros)

def modificar_miembro(id_miembro, nuevos_datos):
	miembros = cargar_datos(RUTA_JSON_MIEMBROS)
	for m in miembros:
		if m['id_miembro'] == id_miembro:
			m.update(nuevos_datos)
			guardar_datos(RUTA_JSON_MIEMBROS, miembros)
			return
	raise ValueError('Miembro no encontrado.')

def eliminar_miembro(id_miembro):
	miembros = cargar_datos(RUTA_JSON_MIEMBROS)
	miembros_nuevos = [m for m in miembros if m['id_miembro'] != id_miembro]
	if len(miembros) == len(miembros_nuevos):
		raise ValueError('Miembro no encontrado.')
	guardar_datos(RUTA_JSON_MIEMBROS, miembros_nuevos)