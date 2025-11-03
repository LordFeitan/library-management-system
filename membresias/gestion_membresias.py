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

RUTA_JSON_PRESTAMOS = 'datos/prestamos.json'

def listar_prestamos():
	datos = cargar_datos(RUTA_JSON_PRESTAMOS)
	return datos

def registrar_prestamo(id_prestamo, id_miembro, id_libro):
	prestamos = cargar_datos(RUTA_JSON_PRESTAMOS)
	miembros = cargar_datos(RUTA_JSON_MIEMBROS)
	libro = buscar_libro_por_id(id_libro)
	
	if not libro:  #excepciones agregadas
		raise LibroNoEncontradoError(f'Libro con ID {id_libro} no encontrado.')
	
	if not libro.get('disponible', True):
		raise LibroNoDisponibleError(f'El libro {libro.get("titulo", id_libro)} no está disponible.')
	
	miembro = next((m for m in miembros if m['id_miembro'] == id_miembro), None)
	if not miembro:
		raise MiembroNoEncontradoError(f'Miembro con ID {id_miembro} no encontrado.')
	
	if any(p['libro']['id'] == id_libro and not p.get('fecha_devolucion') for p in prestamos):
		raise PrestamoActivoError(f'El libro {libro.get("titulo", id_libro)} ya está prestado.')
	
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

def verificar_penalizaciones(id_miembro):
    """Verifica si un miembro tiene penalizaciones pendientes"""
    prestamos = cargar_datos(RUTA_JSON_PRESTAMOS)
    prestamos_miembro = [p for p in prestamos if p['miembro']['id_miembro'] == id_miembro and not p.get('fecha_devolucion')]
    
    for prestamo_data in prestamos_miembro:
        # Crear objeto Prestamo para calcular retrasos
        fecha_prestamo = date.fromisoformat(prestamo_data['fecha_prestamo'])
        prestamo_obj = Prestamo(
            prestamo_data['id_prestamo'],
            Miembro(**prestamo_data['miembro']),
            None,  # No necesitamos el objeto libro completo
            fecha_prestamo
        )
        
        if prestamo_obj.esta_retrasado:
            return True
    return False

def aplicar_penalizacion_automatica(id_prestamo):
    """Aplica penalización automática al devolver un préstamo retrasado"""
    prestamos = cargar_datos(RUTA_JSON_PRESTAMOS)
    for prestamo_data in prestamos:
        if prestamo_data['id_prestamo'] == id_prestamo:
            # Crear objeto Prestamo para el cálculo
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
                # Aplicar penalización combinada
                penalizacion = PenalizacionCombinada(prestamo_obj, prestamo_obj.dias_retraso)
                resultado = penalizacion.aplicar_penalizacion()
                
                print(f"🚨 PENALIZACIÓN APLICADA:")
                print(f"   - Multa: ${resultado['multa']:.2f}")
                print(f"   - Suspensión: {resultado['dias_suspension']} días")
                print(f"   - Días de retraso: {prestamo_obj.dias_retraso}")
                
                return resultado
    return None

def devolver_prestamo(id_prestamo):
    prestamos = cargar_datos(RUTA_JSON_PRESTAMOS)
    for p in prestamos:
        if p['id_prestamo'] == id_prestamo and not p.get('fecha_devolucion'):
            p['fecha_devolucion'] = str(date.today())
            
            # Marcar libro como disponible
            id_libro = p['libro']['id']
            modificar_libro(id_libro, {'disponible': True})
            
            # Verificar y aplicar penalización si hay retraso
            penalizacion = aplicar_penalizacion_automatica(id_prestamo)
            
            guardar_datos(RUTA_JSON_PRESTAMOS, prestamos)
            
            if penalizacion:
                return {'estado': 'devuelto_con_penalizacion', 'penalizacion': penalizacion}
            else:
                return {'estado': 'devuelto_sin_penalizacion'}
                
    raise PrestamoActivoError('Préstamo no encontrado o ya devuelto.')

def listar_prestamos_retrasados():
    """Lista todos los préstamos que están retrasados"""
    prestamos = cargar_datos(RUTA_JSON_PRESTAMOS)
    prestamos_retrasados = []
    
    for prestamo_data in prestamos:
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

def listar_miembros():
	datos = cargar_datos(RUTA_JSON_MIEMBROS)
	return [Miembro(m['id_miembro'], m['nombre'], m['correo'], m['telefono']) for m in datos]

def buscar_miembro_por_id(id_miembro):
	miembros = cargar_datos(RUTA_JSON_MIEMBROS)
	for m in miembros:
		if m['id_miembro'] == id_miembro:
			return m
	return None

def guardar_miembros_ordenados(miembros):   #agregada función
    """Guarda los miembros ordenados por ID"""
    miembros_ordenados = sorted(miembros, key=lambda x: x['id_miembro'])
    guardar_datos(RUTA_JSON_MIEMBROS, miembros_ordenados)

def agregar_miembro(miembro: Miembro): #desde aqui se realizo algunos cambios
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

