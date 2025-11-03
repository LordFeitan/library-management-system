def print_table(headers, rows):   #Función para imprimir tablas en consola
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(headers, *rows)]
    fmt = ' | '.join('{{:{}}}'.format(w) for w in col_widths)
    sep = '-+-'.join('-' * w for w in col_widths)
    print(fmt.format(*headers))
    print(sep)
    for row in rows:
        print(fmt.format(*row))
# Archivo principal para la simulación del sistema de biblioteca

from libros.gestion_libros import listar_libros, agregar_libro, modificar_libro, eliminar_libro, buscar_libro_por_id
from libros.libro import Libro
from libros.autor import Autor
from libros.categoria import Categoria
from libros.validaciones_libros import validar_isbn, validar_titulo, validar_anio, validar_autor, validar_categoria
from membresias.gestion_membresias import listar_miembros, agregar_miembro, modificar_miembro, eliminar_miembro, buscar_miembro_por_id, listar_prestamos, registrar_prestamo, devolver_prestamo, listar_prestamos_retrasados
from membresias.miembro import Miembro
from membresias.validaciones_membresias import validar_id_miembro, validar_nombre, validar_correo, validar_telefono

from membresias.excepciones import (
    MiembroNoEncontradoError, 
    IDDuplicadoError,
    LibroNoEncontradoError,
    LibroNoDisponibleError, 
    PrestamoActivoError
)

def prompt_enter():
    """Espera que el usuario presione Enter para continuar"""
    try:
        input("\n Presiona Enter para continuar...")
    except KeyboardInterrupt:
        print("\n\n Operación cancelada por el usuario")
        exit()

def menu_miembros():
    while True:
        print("\n--- GESTIÓN DE MIEMBROS ---")
        print("1. Listar miembros(tabla)")
        print("2. Agregar miembro")
        print("3. Modificar miembro")
        print("4. Eliminar miembro")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        match opcion:
            case '1':
                miembros = listar_miembros()
                if not miembros:
                    print("❌ No hay miembros registrados.")
                else:
                    headers = ["ID", "Nombre", "Correo", "Teléfono"]
                    rows = [
                        [m.id_miembro, m.nombre, m.correo, m.telefono]  
                        for m in miembros
                    ]
                    print("\n------------- LISTA DE MIEMBROS -------------\n") #Cambio aqui
                    print_table(headers, rows)
                prompt_enter()

            case '2':
                try:
                    print("\n---Ingrese los datos del nuevo miembro---")

                    while True:
                        id_miembro = input("ID: ").strip()
                        try:
                            validar_id_miembro(id_miembro)  
                            id_miembro = id_miembro.upper()
                            
                            # Verificar si ID existe
                            if buscar_miembro_por_id(id_miembro):
                                print(f"❌ Error: ID ya existe. Por favor ingrese un ID diferente.")
                            else:
                                break 

                        except ValueError as e:
                            print(f"❌ Error en el ID: {e}")
                    
                    nombre = input("Nombre: ").strip()
                    validar_nombre(nombre) 
                    nombre = ' '.join(nombre.split()).title()
                    
                    correo = input("Correo: ").strip()
                    validar_correo(correo)  
                    correo = correo.lower()
                    
                    telefono = input("Teléfono: ").strip()
                    validar_telefono(telefono)  
                    telefono = telefono.replace(" ", "")
                    
                    miembro = Miembro(id_miembro, nombre, correo, telefono)
                    agregar_miembro(miembro)
                    print("✅ Miembro agregado correctamente.")

                except IDDuplicadoError as e:  # ← Capturar excepción específica
                    print(f"{e}")
                except ValueError as e:  # ← Capturar errores de validación
                    print(f"❌ Error en los datos: {e}")
                except Exception as e:
                    print(f"❌ Error inesperado: {e}")
                prompt_enter()

            case '3':
                try:
                    id_miembro = input("ID del miembro a modificar: ")
                    id_miembro_normalizado = id_miembro.upper().strip()  # Asegura que el ID esté en mayúsculas -----cambio realizado

                    miembro = buscar_miembro_por_id(id_miembro_normalizado) #cambio aqui

                    if not miembro:
                        print("❌ Miembro no encontrado")
                        prompt_enter()
                        continue 

                    print("\nDeje en blanco para mantener el valor actual.")

                     # Capturar nuevos datos con validación inmediata
                    nuevo_nombre = input(f"\nNuevo nombre [{miembro['nombre']}]: ").strip()
                    if nuevo_nombre:
                        validar_nombre(nuevo_nombre)
                        nuevo_nombre = ' '.join(nuevo_nombre.split()).title()
                    else:
                        nuevo_nombre = miembro['nombre']

                    nuevo_correo = input(f"Nuevo correo [{miembro['correo']}]: ").strip()
                    if nuevo_correo:
                        validar_correo(nuevo_correo)
                        nuevo_correo = nuevo_correo.lower()
                    else:
                        nuevo_correo = miembro['correo']

                    nuevo_telefono = input(f"Nuevo teléfono [{miembro['telefono']}]: ").strip()
                    if nuevo_telefono:
                        validar_telefono(nuevo_telefono)
                        nuevo_telefono = nuevo_telefono.replace(" ", "")
                    else:
                        nuevo_telefono = miembro['telefono']

                    nuevos_datos = {
                        'nombre': nuevo_nombre,
                        'correo': nuevo_correo,
                        'telefono': nuevo_telefono
                    }

                    # MOSTRAR RESUMEN DE CAMBIOS ANTES DE CONFIRMAR
                    print("\n--- Resumen de cambios ---")
                    print(f"ID: {miembro['id_miembro']} (no modificable)")
                    
                    if nuevo_nombre != miembro['nombre']:
                        print(f"Nombre: {miembro['nombre']} → {nuevo_nombre} (MODIFICADO)")
                    else:
                        print(f"Nombre: {nuevo_nombre} (sin cambios)")
                        
                    if nuevo_correo != miembro['correo']:
                        print(f"Correo: {miembro['correo']} → {nuevo_correo} (MODIFICADO)")
                    else:
                        print(f"Correo: {nuevo_correo} (sin cambios)")
                        
                    if nuevo_telefono != miembro['telefono']:
                        print(f"Teléfono: {miembro['telefono']} → {nuevo_telefono} (MODIFICADO)")
                    else:
                        print(f"Teléfono: {nuevo_telefono} (sin cambios)")

                    #CONFIRMACIÓN FINAL
                    confirmar = input("\n" \
                    "¿Confirmar los cambios? (s/n): ").lower()
                    if confirmar != 's':
                        print("❌ Modificación cancelada.")
                        prompt_enter()
                        continue

                    modificar_miembro(id_miembro_normalizado, nuevos_datos)
                    print("✅ Miembro modificado correctamente.")

                except MiembroNoEncontradoError as e:  # ← Capturar excepción específica
                    print(f" {e}")
                except ValueError as e:
                    print(f"❌ Error en los datos: {e}")
                except Exception as e:
                    print(f"❌ Error inesperado: {e}")
                prompt_enter()

            case '4':
                try:
                    id_miembro = input("ID del miembro a eliminar: ")
                    eliminar_miembro(id_miembro.upper())  # Asegura que el ID esté en mayúsculas -----cambio realizado
                    print("✅ Miembro eliminado correctamente.")
                except MiembroNoEncontradoError as e:  # ← Capturar excepción específica
                    print(f"{e}")
                except Exception as e:
                    print(f"❌ Error inesperado: {e}")
                prompt_enter()

            case '5':
                break
                
            case _:
                print("Opción no válida.")
                prompt_enter()

def menu_prestamos():
    while True:
        print("\n--- Gestión de Préstamos ---")
        print("1. Listar préstamos (tabla)")
        print("2. Registrar préstamo")
        print("3. Devolver préstamo")
        print("4. Ver préstamos retrasados")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        match opcion:
            case '1':
                prestamos = listar_prestamos()
                if not prestamos:
                    print("No hay préstamos registrados.")
                else:
                    headers = ["ID Préstamo", "Libro", "Miembro", "Fecha Préstamo", "Devuelto"]
                    rows = [
                        [
                            p['id_prestamo'],
                            p['libro']['titulo'] if isinstance(p['libro'], dict) else str(p['libro']),
                            p['miembro']['nombre'] if isinstance(p['miembro'], dict) else str(p['miembro']),
                            p['fecha_prestamo'],
                            "Sí" if p.get('fecha_devolucion') else "No"
                        ] for p in prestamos
                    ]
                    print_table(headers, rows)
                prompt_enter()

            case '2':
                try:
                    id_prestamo = input("ID de préstamo: ")
                    id_miembro = input("ID de miembro: ")
                    id_miembro = id_miembro.upper()  # Asegura que el ID esté en mayúsculas -----cambio realizado2
                    id_libro = input("ID del libro: ")
                    registrar_prestamo(id_prestamo, id_miembro, id_libro)
                    print("Préstamo registrado correctamente.")
                except (LibroNoEncontradoError, LibroNoDisponibleError, MiembroNoEncontradoError, PrestamoActivoError) as e:  # ← Múltiples excepciones
                    print(f"{e}")
                except ValueError as e:
                    print(f"Error en los datos: {e}")
                except Exception as e:
                    print(f"Error inesperado: {e}")
                prompt_enter()

            case '3':
                try:
                    id_prestamo = input("ID del préstamo a devolver: ")
                    resultado = devolver_prestamo(id_prestamo)
                    
                    if resultado['estado'] == 'devuelto_con_penalizacion':
                        print("✅ Préstamo devuelto correctamente.")
                        print("⚠️  Se aplicó penalización por retraso.")
                    else:
                        print("✅ Préstamo devuelto correctamente.")
                        
                except PrestamoActivoError as e:
                    print(f"{e}")
                except Exception as e:
                    print(f"Error inesperado: {e}")
                prompt_enter()

            case '4':  # Agrega esta opción en el menú
                prestamos_retrasados = listar_prestamos_retrasados()
                if not prestamos_retrasados:
                    print("✅ No hay préstamos retrasados.")
                else:
                    print(f"🚨 PRÉSTAMOS RETRASADOS ({len(prestamos_retrasados)})")
                    headers = ["ID Préstamo", "Libro", "Miembro", "Días Retraso", "Multa Estimada"]
                    rows = []
                    for item in prestamos_retrasados:
                        p = item['prestamo']
                        dias_retraso = item['dias_retraso']
                        multa_estimada = dias_retraso * 1.0  # $1 por día
                        rows.append([
                            p['id_prestamo'],
                            p['libro']['titulo'],
                            p['miembro']['nombre'],
                            dias_retraso,
                            f"${multa_estimada:.2f}"
                        ])
                    print_table(headers, rows)
                prompt_enter()

            case '5':
                break
            case _:
                print("Opción no válida.")
                prompt_enter()


def menu_libros():
    while True:
        print("\n--- Gestión de Libros ---")
        print("1. Listar libros")
        print("2. Agregar libro")
        print("3. Modificar libro")
        print("4. Eliminar libro")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ")
        match opcion:
            case '1':
                libros = listar_libros()
                if not libros:
                    print("No hay libros registrados.")
                else:
                    headers = ["ID", "Título", "Autor", "Categoría", "Año", "Disponible"]
                    rows = [
                        [
                            libro.id,
                            libro.titulo,
                            str(libro.autor),
                            libro.categoria,
                            libro.anio,
                            "Sí" if libro.disponible else "No"
                        ] for libro in libros
                    ]
                    print_table(headers, rows)
                prompt_enter()

            case '2':
                try:
                    id_libro = input("ID: ")
                    # Validar id_libro si es necesario
                    titulo = input("Título: ")
                    validar_titulo(titulo)
                    autor_nombre = input("Nombre del autor: ")
                    autor_nac = input("Nacionalidad del autor: ")
                    autor = Autor(autor_nombre, autor_nac)
                    validar_autor(autor)
                    categoria = input("Categoría: ")
                    # Si se requiere validación de categoría, agregar aquí
                    anio = int(input("Año de publicación: "))
                    validar_anio(anio)
                    libro = Libro(id_libro, titulo, autor, categoria, anio)
                    agregar_libro(libro)
                    print("Libro agregado correctamente.")
                except Exception as e:
                    print(f"Error: {e}")
                prompt_enter()

            case '3':
                try:
                    id_libro = input("ID del libro a modificar: ")
                    libro = buscar_libro_por_id(id_libro)
                    if not libro:
                        print("Libro no encontrado.")
                        continue
                    print("Deje en blanco para mantener el valor actual.")
                    nuevo_titulo = input(f"Nuevo título [{libro['titulo']}]: ") or libro['titulo']
                    nuevo_categoria = input(f"Nueva categoría [{libro['categoria']}]: ") or libro['categoria']
                    nuevo_anio = input(f"Nuevo año [{libro['anio']}]: ") or libro['anio']
                    nuevo_disp = input(f"¿Disponible? (s/n) [{ 's' if libro.get('disponible', True) else 'n' }]: ")
                    nuevos_datos = {
                        'titulo': nuevo_titulo,
                        'categoria': nuevo_categoria,
                        'anio': int(nuevo_anio),
                        'disponible': (nuevo_disp.lower() == 's') if nuevo_disp else libro.get('disponible', True)
                    }
                    modificar_libro(id_libro, nuevos_datos)
                    print("Libro modificado correctamente.")
                except Exception as e:
                    print(f"Error: {e}")
                prompt_enter()

            case '4':
                try:
                    id_libro = input("ID del libro a eliminar: ")
                    eliminar_libro(id_libro)
                    print("Libro eliminado correctamente.")
                except Exception as e:
                    print(f"Error: {e}")
            case '5':
                break
            case _:
                print("Opción no válida.")
                prompt_enter()



def menu_principal():
    while True:
        print("\n=== Sistema de Biblioteca ===")
        print("1. Gestión de libros")
        print("2. Gestión de miembros")
        print("3. Gestión de préstamos")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")
        match opcion:
            case '1':
                menu_libros()
            case '2':
                menu_miembros()
            case '3':
                menu_prestamos()
            case '4':
                print("¡Hasta luego!")
                break
            case _:
                print("Opción no válida.")

if __name__ == "__main__":
    menu_principal()
