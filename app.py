def confirmar_salida():
    respuesta = input("¿Seguro que deseas salir? (s/n): ").strip().lower()
    if respuesta == 's':
        print("¡Hasta luego!")
        exit()
    elif respuesta == 'n':
        return
    else:
        print("Respuesta no válida. Intenta de nuevo.")
        confirmar_salida()
from libros.gestion_libros import (
    listar_libros, agregar_libro, modificar_libro, eliminar_libro, buscar_libro_por_id
)
from libros.libro import Libro
from libros.autor import Autor
from libros.categoria import Categoria
from libros.validaciones_libros import validar_id_libro, validar_titulo, validar_anio, validar_autor, validar_categoria

from membresias.gestion_membresias import (
    listar_miembros, agregar_miembro, modificar_miembro, eliminar_miembro,
    buscar_miembro_por_id, listar_prestamos, registrar_prestamo, devolver_prestamo,
    listar_prestamos_retrasados
)
from membresias.miembro import Miembro
from membresias.validaciones_membresias import validar_id_miembro, validar_nombre, validar_correo, validar_telefono

from membresias.excepciones import (
    MiembroNoEncontradoError,
    IDDuplicadoError,
    LibroNoEncontradoError,
    LibroNoDisponibleError,
    PrestamoActivoError
)


def print_table(headers, rows):
    if not rows:
        print("(sin resultados)")
        return
    col_widths = [max(len(str(cell)) for cell in col)
                  for col in zip(headers, *rows)]
    fmt = ' | '.join('{{:{}}}'.format(w) for w in col_widths)
    sep = '-+-'.join('-' * w for w in col_widths)
    print(fmt.format(*headers))
    print(sep)
    for row in rows:
        print(fmt.format(*row))


def prompt_enter():
    """Espera que el usuario presione Enter para continuar"""
    try:
        input("\n Presiona Enter para continuar...")
    except KeyboardInterrupt:
        print("\n\n Operación cancelada por el usuario")
        exit()


def pedir_id_no_existente(buscar_funcion, mensaje="ID: "):
    """Pide un ID hasta que NO exista en el sistema. Devuelve ID en mayúsculas."""
    while True:
        id_ingresado = input(mensaje).strip().upper()
        if not id_ingresado:
            print("❌ El ID no puede estar vacío.")
            continue
        try:
            # Si se está usando para libros, validar con validar_id_libro
            if buscar_funcion.__name__ == 'buscar_libro_por_id':
                validar_id_libro(id_ingresado)
            else:
                validar_id_miembro(id_ingresado)
        except Exception as e:
            print(f"❌ {e}")
            continue
        existe = buscar_funcion(id_ingresado)
        if not existe:
            return id_ingresado
        print("❌ Ese ID ya existe, ingrese otro.")


def pedir_id_existente(buscar_funcion, mensaje="ID: ", comprobar_activo=False):
    """
    Pide un ID hasta que exista en el sistema.
    comprobar_activo: opcional, si True espera que el recurso exista y esté 'activo' (p.ej. préstamo no devuelto).
    """
    while True:
        id_ingresado = input(mensaje).strip().upper()
        if not id_ingresado:
            print("❌ El ID no puede estar vacío.")
            continue
        registro = buscar_funcion(id_ingresado)
        if not registro:
            print("❌ Ese ID no existe, intente nuevamente.")
            continue

        if comprobar_activo:

            prestamos = listar_prestamos()
            prest = next(
                (p for p in prestamos if p['id_prestamo'] == id_ingresado), None)
            if not prest:
                print("❌ Préstamo no encontrado, intente nuevamente.")
                continue
            if prest.get('fecha_devolucion'):
                print("❌ El préstamo ya está devuelto. Ingrese un préstamo activo.")
                continue
        return id_ingresado


def menu_miembros():
    while True:
        print("\n--- GESTIÓN DE MIEMBROS ---")
        print("1. Listar miembros (tabla)")
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
                    print("\n------------- LISTA DE MIEMBROS -------------\n")
                    print_table(headers, rows)
                prompt_enter()

            case '2':
                try:
                    print("\n--- Ingrese los datos del nuevo miembro ---")
                    id_miembro = pedir_id_no_existente(
                        lambda x: buscar_miembro_por_id(x), "ID: ")

                    while True:
                        nombre = input("Nombre: ").strip()
                        try:
                            validar_nombre(nombre)
                            nombre = ' '.join(nombre.split()).title()
                            break
                        except Exception as e:
                            print(f"❌ {e}")

                    while True:
                        correo = input("Correo: ").strip()
                        try:
                            validar_correo(correo)
                            correo = correo.lower()
                            break
                        except Exception as e:
                            print(f"❌ {e}")

                    while True:
                        telefono = input("Teléfono: ").strip()
                        try:
                            validar_telefono(telefono)
                            telefono = telefono.replace(" ", "")
                            break
                        except Exception as e:
                            print(f"❌ {e}")

                    miembro = Miembro(id_miembro, nombre, correo, telefono)
                    agregar_miembro(miembro)
                    print("✅ Miembro agregado correctamente.")

                except IDDuplicadoError as e:
                    print(f"{e}")
                except ValueError as e:
                    print(f"❌ Error en los datos: {e}")
                except Exception as e:
                    print(f"❌ Error inesperado: {e}")
                prompt_enter()

            case '3':
                try:
                    id_miembro = pedir_id_existente(lambda x: buscar_miembro_por_id(x),
                                                    "ID del miembro a modificar: ")
                    miembro = buscar_miembro_por_id(id_miembro)
                    if not miembro:
                        print("❌ Miembro no encontrado")
                        prompt_enter()
                        continue

                    print("\nDeje en blanco para mantener el valor actual.")

                    nuevo_nombre = input(
                        f"\nNuevo nombre [{miembro['nombre']}]: ").strip()
                    if nuevo_nombre:
                        validar_nombre(nuevo_nombre)
                        nuevo_nombre = ' '.join(nuevo_nombre.split()).title()
                    else:
                        nuevo_nombre = miembro['nombre']

                    nuevo_correo = input(
                        f"Nuevo correo [{miembro['correo']}]: ").strip()
                    if nuevo_correo:
                        validar_correo(nuevo_correo)
                        nuevo_correo = nuevo_correo.lower()
                    else:
                        nuevo_correo = miembro['correo']

                    nuevo_telefono = input(
                        f"Nuevo teléfono [{miembro['telefono']}]: ").strip()
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

                    print("\n--- Resumen de cambios ---")
                    print(f"ID: {miembro['id_miembro']} (no modificable)")
                    if nuevo_nombre != miembro['nombre']:
                        print(
                            f"Nombre: {miembro['nombre']} → {nuevo_nombre} (MODIFICADO)")
                    else:
                        print(f"Nombre: {nuevo_nombre} (sin cambios)")

                    if nuevo_correo != miembro['correo']:
                        print(
                            f"Correo: {miembro['correo']} → {nuevo_correo} (MODIFICADO)")
                    else:
                        print(f"Correo: {nuevo_correo} (sin cambios)")

                    if nuevo_telefono != miembro['telefono']:
                        print(
                            f"Teléfono: {miembro['telefono']} → {nuevo_telefono} (MODIFICADO)")
                    else:
                        print(f"Teléfono: {nuevo_telefono} (sin cambios)")

                    confirmar = input(
                        "\n¿Confirmar los cambios? (s/n): ").lower()
                    if confirmar != 's':
                        print("❌ Modificación cancelada.")
                        prompt_enter()
                        continue

                    modificar_miembro(id_miembro, nuevos_datos)
                    print("✅ Miembro modificado correctamente.")

                except MiembroNoEncontradoError as e:
                    print(f"{e}")
                except ValueError as e:
                    print(f"❌ Error en los datos: {e}")
                except Exception as e:
                    print(f"❌ Error inesperado: {e}")
                prompt_enter()

            case '4':
                try:
                    id_miembro = pedir_id_existente(lambda x: buscar_miembro_por_id(x),
                                                    "ID del miembro a eliminar: ")
                    eliminar_miembro(id_miembro)
                    print("✅ Miembro eliminado correctamente.")
                except MiembroNoEncontradoError as e:
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
                    headers = ["ID Préstamo", "Libro",
                               "Miembro", "Fecha Préstamo", "Devuelto"]
                    rows = [
                        [
                            p['id_prestamo'],
                            p['libro']['titulo'] if isinstance(
                                p['libro'], dict) else str(p['libro']),
                            p['miembro']['nombre'] if isinstance(
                                p['miembro'], dict) else str(p['miembro']),
                            p['fecha_prestamo'],
                            "Sí" if p.get('fecha_devolucion') else "No"
                        ] for p in prestamos
                    ]
                    print_table(headers, rows)
                prompt_enter()

            case '2':
                try:

                    id_prestamo = pedir_id_no_existente(lambda x: any(p['id_prestamo'] == x for p in listar_prestamos()),
                                                        "ID de préstamo: ")
                    id_miembro = pedir_id_existente(
                        lambda x: buscar_miembro_por_id(x), "ID de miembro: ")
                    id_libro = pedir_id_existente(
                        lambda x: buscar_libro_por_id(x), "ID del libro: ")

                    registrar_prestamo(id_prestamo, id_miembro, id_libro)
                    print("Préstamo registrado correctamente.")
                except (LibroNoEncontradoError, LibroNoDisponibleError, MiembroNoEncontradoError, PrestamoActivoError) as e:
                    print(f"{e}")
                except ValueError as e:
                    print(f"Error en los datos: {e}")
                except Exception as e:
                    print(f"Error inesperado: {e}")
                prompt_enter()

            case '3':
                try:
                    id_prestamo = pedir_id_existente(lambda x: any(p['id_prestamo'] == x for p in listar_prestamos()),
                                                     "ID del préstamo a devolver: ", comprobar_activo=True)
                    resultado = devolver_prestamo(id_prestamo)

                    if isinstance(resultado, dict) and resultado.get('estado') == 'devuelto_con_penalizacion':
                        print("✅ Préstamo devuelto correctamente.")
                        print("⚠️  Se aplicó penalización por retraso.")
                    else:
                        print("✅ Préstamo devuelto correctamente.")

                except PrestamoActivoError as e:
                    print(f"{e}")
                except Exception as e:
                    print(f"Error inesperado: {e}")
                prompt_enter()

            case '4':
                prestamos_retrasados = listar_prestamos_retrasados()
                if not prestamos_retrasados:
                    print("✅ No hay préstamos retrasados.")
                else:
                    print(
                        f"🚨 PRÉSTAMOS RETRASADOS ({len(prestamos_retrasados)})")
                    headers = ["ID Préstamo", "Libro", "Miembro",
                               "Días Retraso", "Multa Estimada"]
                    rows = []
                    for item in prestamos_retrasados:
                        p = item['prestamo']
                        dias_retraso = item['dias_retraso']
                        multa_estimada = dias_retraso * 1.0 
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
                    headers = ["ID", "Título", "Autor",
                               "Categoría", "Año", "Disponible"]
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
                    id_libro = pedir_id_no_existente(lambda x: buscar_libro_por_id(x),
                                                     "ID: ")
                    while True:
                        titulo = input("Título: ").strip()
                        try:
                            validar_titulo(titulo)
                            break
                        except Exception as e:
                            print(f"❌ {e}")

                    autor_nombre = input("Nombre del autor: ").strip()
                    autor_nac = input("Nacionalidad del autor: ").strip()
                    autor = Autor(autor_nombre, autor_nac)
                    try:
                        validar_autor(autor)
                    except Exception as e:
                        print(f"❌ {e}")
                        prompt_enter()
                        continue

                    categoria = input("Categoría: ").strip()
                    try:
                        validar_categoria(categoria)
                    except Exception:
        
                        pass

                    while True:
                        try:
                            anio = int(input("Año de publicación: ").strip())
                            validar_anio(anio)
                            break
                        except ValueError:
                            print("❌ El año debe ser un número.")
                        except Exception as e:
                            print(f"❌ {e}")

                    libro = Libro(id_libro, titulo, autor, categoria, anio)
                    agregar_libro(libro)
                    print("✅ Libro agregado correctamente.")
                except Exception as e:
                    print(f"Error: {e}")
                prompt_enter()

            case '3':
                try:
                    id_libro = pedir_id_existente(lambda x: buscar_libro_por_id(x),
                                                  "ID del libro a modificar: ")
                    libro = buscar_libro_por_id(id_libro)
                    if not libro:
                        print("Libro no encontrado.")
                        continue
                    print("Deje en blanco para mantener el valor actual.")
                    nuevo_titulo = input(
                        f"Nuevo título [{libro['titulo']}]: ").strip() or libro['titulo']
                    nuevo_categoria = input(
                        f"Nueva categoría [{libro['categoria']}]: ").strip() or libro['categoria']
                    nuevo_anio_input = input(
                        f"Nuevo año [{libro['anio']}]: ").strip()
                    nuevo_anio = int(
                        nuevo_anio_input) if nuevo_anio_input else libro['anio']
                    nuevo_disp = input(
                        f"¿Disponible? (s/n) [{'s' if libro.get('disponible', True) else 'n'}]: ").strip()
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
                    id_libro = pedir_id_existente(lambda x: buscar_libro_por_id(x),
                                                  "ID del libro a eliminar: ")
                    eliminar_libro(id_libro)
                    print("Libro eliminado correctamente.")
                except Exception as e:
                    print(f"Error: {e}")
                prompt_enter()
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
                confirmar_salida()
            case _:
                print("Opción no válida.")


if __name__ == "__main__":
    menu_principal()
