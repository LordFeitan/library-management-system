# Operaciones CRUD de libros
from datos.json_manager import cargar_datos, guardar_datos
from .libro import Libro
from .autor import Autor
from .categoria import Categoria

RUTA_JSON = 'datos/libros.json'

def listar_libros():
	datos = cargar_datos(RUTA_JSON)
	libros = []
	errores = []
	for idx, l in enumerate(datos):
		try:
			libro = Libro(
				l['id'],
				l['titulo'],
				Autor(l['autor']['nombre'], l['autor']['nacionalidad']),
				l['categoria'],
				l['anio'],
				l.get('disponible', True)
			)
			# inyectar stock para que la UI pueda mostrarlo
			setattr(libro, 'stock', l.get('stock', 0))
			libros.append(libro)
		except Exception as e:
			errores.append(f"Error en libro #{idx+1}: {e}")
	if errores:
		print("\nSe encontraron errores al cargar algunos libros:")
		for err in errores:
			print(err)
	return libros

def generar_siguiente_id_libro():
	"""Genera el siguiente ID de libro automáticamente (L001, L002, ...)"""
	libros = cargar_datos(RUTA_JSON)
	if not libros:
		return 'L001'
	
	# Extraer números de los IDs existentes
	numeros = []
	for libro in libros:
		id_str = libro['id']
		if id_str.startswith('L') and len(id_str) > 1:
			try:
				numeros.append(int(id_str[1:]))
			except ValueError:
				continue
	
	if not numeros:
		return 'L001'
	
	siguiente_numero = max(numeros) + 1
	return f'L{siguiente_numero:03d}'

def buscar_libro_por_id(id_libro):
	libros = cargar_datos(RUTA_JSON)
	for l in libros:
		if l['id'] == id_libro:
			return l
	return None

def agregar_libro(libro: Libro):
	libros = cargar_datos(RUTA_JSON)
	if any(l['id'] == libro.id for l in libros):
		raise ValueError('Ya existe un libro con ese ID.')
	libros.append({
		'id': libro.id,
		'titulo': libro.titulo,
		'autor': {'nombre': libro.autor.nombre, 'nacionalidad': libro.autor.nacionalidad},
		'categoria': libro.categoria,
		'anio': libro.anio,
		'stock': getattr(libro, 'stock', 1)
	})
	guardar_datos(RUTA_JSON, libros)

def modificar_libro(id_libro, nuevos_datos):
	libros = cargar_datos(RUTA_JSON)
	for l in libros:
		if l['id'] == id_libro:
			l.update(nuevos_datos)
			guardar_datos(RUTA_JSON, libros)
			return
	raise ValueError('Libro no encontrado.')

def eliminar_libro(id_libro):
	libros = cargar_datos(RUTA_JSON)
	libros_nuevos = [l for l in libros if l['id'] != id_libro]
	if len(libros) == len(libros_nuevos):
		raise ValueError('Libro no encontrado.')
	guardar_datos(RUTA_JSON, libros_nuevos)