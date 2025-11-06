# Gestión de préstamos y miembros
from datos.json_manager import cargar_datos, guardar_datos
from .miembro import Miembro
from libros.gestion_libros import buscar_libro_por_id, modificar_libro
from .prestamo import Prestamo
from datetime import date

# IMPORTAR EXCEPCIONES PERSONALIZADAS
from .excepciones import (
    MiembroNoEncontradoError, 
    IDDuplicadoError, 
    LibroNoEncontradoError,
    LibroNoDisponibleError,
    PrestamoActivoError
)

#IMPORTAR PENALIZACIONES
from .penalizaciones import PenalizacionCombinada



def listar_prestamos():
    # Nuevo: Listar todos los préstamos recorriendo los miembros
    miembros = cargar_datos(RUTA_JSON_MIEMBROS)
    prestamos = []
    for miembro in miembros:
        for prestamo in miembro.get('prestamos', []):
            prestamo_copia = prestamo.copy()
            prestamo_copia['miembro'] = {'id_miembro': miembro['id_miembro'], 'nombre': miembro['nombre']}
            prestamos.append(prestamo_copia)
    return prestamos

def registrar_prestamo(id_prestamo, id_miembro, id_libro):
    miembros = cargar_datos(RUTA_JSON_MIEMBROS)
    libro = buscar_libro_por_id(id_libro)

    if not libro:
        raise LibroNoEncontradoError(f'Libro con ID {id_libro} no encontrado.')

    stock_actual = int(libro.get('stock', 0))
    if stock_actual <= 0:
        raise LibroNoDisponibleError(f'No hay stock disponible para el libro {libro.get("titulo", id_libro)}.')

    miembro = next((m for m in miembros if m['id_miembro'] == id_miembro), None)
    if not miembro:
        raise MiembroNoEncontradoError(f'Miembro con ID {id_miembro} no encontrado.')

    # Evitar ID de préstamo duplicado en todos los miembros
    if any(p.get('id_prestamo') == id_prestamo for m in miembros for p in m.get('prestamos', [])):
        raise PrestamoActivoError(f'Ya existe un préstamo con ID {id_prestamo}.')

    nuevo_prestamo = {
        'id_prestamo': id_prestamo,
        'miembro': {'id_miembro': miembro['id_miembro'], 'nombre': miembro['nombre']},
        'libro': {'id': libro['id'], 'titulo': libro['titulo']},
        'fecha_prestamo': str(date.today()),
        'fecha_devolucion': None
    }

    # Agregar préstamo al miembro
    miembro.setdefault('prestamos', []).append(nuevo_prestamo)

    # Decrementar stock del libro
    modificar_libro(id_libro, {'stock': stock_actual - 1})

    # Guardar miembros actualizados
    guardar_datos(RUTA_JSON_MIEMBROS, miembros)

def verificar_penalizaciones(id_miembro):
    """Verifica si un miembro tiene penalizaciones pendientes"""
    miembros = cargar_datos(RUTA_JSON_MIEMBROS)
    prestamos_miembro = [
        p for m in miembros if m['id_miembro'] == id_miembro
        for p in m.get('prestamos', []) if not p.get('fecha_devolucion')
    ]
    
    for prestamo_data in prestamos_miembro:
      
        fecha_prestamo = date.fromisoformat(prestamo_data['fecha_prestamo'])
        prestamo_obj = Prestamo(
            prestamo_data['id_prestamo'],
            Miembro(**prestamo_data['miembro']),
            None,  
            fecha_prestamo
        )
        
        if prestamo_obj.esta_retrasado:
            return True
    return False

def aplicar_penalizacion_automatica(id_prestamo):
    """Aplica penalización automática al devolver un préstamo retrasado"""
    miembros = cargar_datos(RUTA_JSON_MIEMBROS)
    for m in miembros:
        for prestamo_data in m.get('prestamos', []):
            if prestamo_data['id_prestamo'] == id_prestamo:
                fecha_prestamo = date.fromisoformat(prestamo_data['fecha_prestamo'])
                fecha_devolucion = date.today()

                prestamo_obj = Prestamo(
                    prestamo_data['id_prestamo'],
                    Miembro(**prestamo_data['miembro']),
                    None,
                    fecha_prestamo,
                    fecha_devolucion
                )

                if prestamo_obj.esta_retrasado:
                    penalizacion = PenalizacionCombinada(prestamo_obj, prestamo_obj.dias_retraso)
                    resultado = penalizacion.aplicar_penalizacion()
                    print(f"🚨 PENALIZACIÓN APLICADA:")
                    print(f"   - Multa: ${resultado['multa']:.2f}")
                    print(f"   - Suspensión: {resultado['dias_suspension']} días")
                    print(f"   - Días de retraso: {prestamo_obj.dias_retraso}")
                    return resultado
    return None

def devolver_prestamo(id_prestamo):
    miembros = cargar_datos(RUTA_JSON_MIEMBROS)
    for m in miembros:
        for p in m.get('prestamos', []):
            if p['id_prestamo'] == id_prestamo and not p.get('fecha_devolucion'):
                p['fecha_devolucion'] = str(date.today())

                id_libro = p['libro']['id']
                libro = buscar_libro_por_id(id_libro)
                stock_actual = int(libro.get('stock', 0)) if libro else 0
                modificar_libro(id_libro, {'stock': stock_actual + 1})

                penalizacion = aplicar_penalizacion_automatica(id_prestamo)

                guardar_datos(RUTA_JSON_MIEMBROS, miembros)

                if penalizacion:
                    return {'estado': 'devuelto_con_penalizacion', 'penalizacion': penalizacion}
                else:
                    return {'estado': 'devuelto_sin_penalizacion'}

    raise PrestamoActivoError('Préstamo no encontrado o ya devuelto.')

def listar_prestamos_retrasados():
    """Lista todos los préstamos que están retrasados"""
    miembros = cargar_datos(RUTA_JSON_MIEMBROS)
    prestamos_retrasados = []

    for m in miembros:
        for prestamo_data in m.get('prestamos', []):
            if not prestamo_data.get('fecha_devolucion'):
                fecha_prestamo = date.fromisoformat(prestamo_data['fecha_prestamo'])
                prestamo_obj = Prestamo(
                    prestamo_data['id_prestamo'],
                    Miembro(**prestamo_data['miembro']),
                    None,
                    fecha_prestamo
                )

                if prestamo_obj.esta_retrasado:
                    prestamos_retrasados.append({
                        'prestamo': prestamo_data,
                        'dias_retraso': prestamo_obj.dias_retraso
                    })

    return prestamos_retrasados

RUTA_JSON_MIEMBROS = 'datos/miembros.json'

def generar_siguiente_id_miembro():
	"""Genera el siguiente ID de miembro automáticamente (M001, M002, ...)"""
	miembros = cargar_datos(RUTA_JSON_MIEMBROS)
	if not miembros:
		return 'M001'
	
	numeros = []
	for miembro in miembros:
		id_str = miembro['id_miembro']
		if id_str.startswith('M') and len(id_str) > 1:
			try:
				numeros.append(int(id_str[1:]))
			except ValueError:
				continue
	
	if not numeros:
		return 'M001'
	
	siguiente_numero = max(numeros) + 1
	return f'M{siguiente_numero:03d}'

def generar_siguiente_id_prestamo():
	"""Genera el siguiente ID de préstamo automáticamente (P001, P002, ...)"""
	prestamos = listar_prestamos()
	if not prestamos:
		return 'P001'
	
	numeros = []
	for prestamo in prestamos:
		id_str = prestamo['id_prestamo']
		if id_str.startswith('P') and len(id_str) > 1:
			try:
				numeros.append(int(id_str[1:]))
			except ValueError:
				continue
	
	if not numeros:
		return 'P001'
	
	siguiente_numero = max(numeros) + 1
	return f'P{siguiente_numero:03d}'

def listar_miembros():
	datos = cargar_datos(RUTA_JSON_MIEMBROS)
	return [Miembro(m['id_miembro'], m['nombre'], m['correo'], m['telefono']) for m in datos]

def buscar_miembro_por_id(id_miembro):
	miembros = cargar_datos(RUTA_JSON_MIEMBROS)
	for m in miembros:
		if m['id_miembro'] == id_miembro:
			return m
	return None

def guardar_miembros_ordenados(miembros): 
    """Guarda los miembros ordenados por ID"""
    miembros_ordenados = sorted(miembros, key=lambda x: x['id_miembro'])
    guardar_datos(RUTA_JSON_MIEMBROS, miembros_ordenados)

def agregar_miembro(miembro: Miembro): 
	miembros = cargar_datos(RUTA_JSON_MIEMBROS)

	if any(m['id_miembro'] == miembro.id_miembro for m in miembros):
		raise IDDuplicadoError(f'Ya existe un miembro con el ID {miembro.id_miembro}.')
	
	miembros.append({
		'id_miembro': miembro.id_miembro,
		'nombre': miembro.nombre, 
		'correo': miembro.correo, 
		'telefono': miembro.telefono  
	})
	guardar_miembros_ordenados(miembros) 

def modificar_miembro(id_miembro, nuevos_datos):
	miembros = cargar_datos(RUTA_JSON_MIEMBROS)
	id_normalizado = id_miembro

	for m in miembros:
		if m['id_miembro'] == id_normalizado:
			m.update(nuevos_datos)
			guardar_miembros_ordenados(miembros)
			return
	raise MiembroNoEncontradoError(f'Miembro con ID {id_miembro} no encontrado.')

def eliminar_miembro(id_miembro):
	miembros = cargar_datos(RUTA_JSON_MIEMBROS)
	id_normalizado = id_miembro

	miembros_nuevos = [m for m in miembros if m['id_miembro'] != id_normalizado]
	if len(miembros) == len(miembros_nuevos):
		raise MiembroNoEncontradoError(f'Miembro con ID {id_miembro} no encontrado.')
	
	guardar_miembros_ordenados(miembros_nuevos)

