from libros.gestion_libros import (
    listar_libros, agregar_libro, modificar_libro, eliminar_libro, buscar_libro_por_id,
    generar_siguiente_id_libro
)
from membresias.excepciones import (
    MiembroNoEncontradoError,
    IDDuplicadoError,
    LibroNoEncontradoError,
    LibroNoDisponibleError,
    PrestamoActivoError
)
from membresias.validaciones_membresias import validar_id_miembro, validar_nombre, validar_correo, validar_telefono
from membresias.miembro import Miembro
from membresias.gestion_membresias import (
    listar_miembros, agregar_miembro, modificar_miembro, eliminar_miembro,
    buscar_miembro_por_id, listar_prestamos, registrar_prestamo, devolver_prestamo,
    listar_prestamos_retrasados, generar_siguiente_id_miembro, generar_siguiente_id_prestamo
)
from libros.validaciones_libros import validar_id_libro, validar_titulo, validar_anio, validar_autor, validar_categoria
from libros.categoria import Categoria
from libros.autor import Autor
from libros.libro import Libro
from libros.gestion_categorias import (
    listar_categorias, agregar_categoria, modificar_categoria, eliminar_categoria,
    buscar_categoria_por_id, buscar_categoria_por_nombre, mostrar_menu_seleccion_categoria
)


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
                    id_miembro = generar_siguiente_id_miembro()
                    print(f"📝 ID generado automáticamente: {id_miembro}")

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
                    miembros = listar_miembros()
                    if not miembros:
                        print("❌ No hay miembros registrados para modificar.")
                        prompt_enter()
                        continue

                    print("\n--- Miembros Disponibles ---")
                    headers = ["ID", "Nombre", "Correo", "Teléfono"]
                    rows = [
                        [m.id_miembro, m.nombre, m.correo, m.telefono]
                        for m in miembros
                    ]
                    print_table(headers, rows)
                    print()

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
                    miembros = listar_miembros()
                    if not miembros:
                        print("❌ No hay miembros registrados para eliminar.")
                        prompt_enter()
                        continue

                    print("\n--- Miembros Disponibles ---")
                    headers = ["ID", "Nombre", "Correo", "Teléfono"]
                    rows = [
                        [m.id_miembro, m.nombre, m.correo, m.telefono]
                        for m in miembros
                    ]
                    print_table(headers, rows)
                    print()

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
                    id_prestamo = generar_siguiente_id_prestamo()
                    print(
                        f"📝 ID de préstamo generado automáticamente: {id_prestamo}")

                    id_miembro = pedir_id_existente(
                        lambda x: buscar_miembro_por_id(x), "ID de miembro: ")
                    id_libro = pedir_id_existente(
                        lambda x: buscar_libro_por_id(x), "ID del libro: ")

                    registrar_prestamo(id_prestamo, id_miembro, id_libro)
                    print("✅ Préstamo registrado correctamente.")
                except (LibroNoEncontradoError, LibroNoDisponibleError, MiembroNoEncontradoError, PrestamoActivoError) as e:
                    print(f"{e}")
                except ValueError as e:
                    print(f"Error en los datos: {e}")
                except Exception as e:
                    print(f"Error inesperado: {e}")
                prompt_enter()

            case '3':
                try:
                    prestamos = listar_prestamos()
                    prestamos_activos = [
                        p for p in prestamos if not p.get('fecha_devolucion')]

                    if not prestamos_activos:
                        print("❌ No hay préstamos activos para devolver.")
                        prompt_enter()
                        continue

                    print("\n--- Préstamos Activos (Pendientes de Devolución) ---")
                    headers = ["ID Préstamo", "Libro",
                               "Miembro", "Fecha Préstamo"]
                    rows = [
                        [
                            p['id_prestamo'],
                            p['libro']['titulo'] if isinstance(
                                p['libro'], dict) else str(p['libro']),
                            p['miembro']['nombre'] if isinstance(
                                p['miembro'], dict) else str(p['miembro']),
                            p['fecha_prestamo']
                        ] for p in prestamos_activos
                    ]
                    print_table(headers, rows)
                    print()

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
                               "Categoría", "Año", "Stock"]
                    rows = []
                    for libro in libros:
                        cat_id = libro.categoria
                        cat = buscar_categoria_por_id(cat_id)
                        cat_nombre = cat['nombre'] if cat else cat_id

                        rows.append([
                            libro.id,
                            libro.titulo,
                            str(libro.autor),
                            cat_nombre,
                            libro.anio,
                            getattr(libro, 'stock', 0)
                        ])
                    print_table(headers, rows)
                prompt_enter()

            case '2':
                try:
                    id_libro = generar_siguiente_id_libro()
                    print(f"📝 ID generado automáticamente: {id_libro}")

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

                    categoria = mostrar_menu_seleccion_categoria()
                    if not categoria:
                        print("❌ Operación cancelada.")
                        prompt_enter()
                        continue

                    try:
                        validar_categoria(categoria)
                    except Exception as e:
                        print(f"❌ {e}")
                        prompt_enter()
                        continue

                    while True:
                        try:
                            stock = int(
                                input("Stock inicial (número entero >= 0): ").strip())
                            if stock < 0:
                                print("❌ El stock no puede ser negativo.")
                                continue
                            break
                        except ValueError:
                            print("❌ El stock debe ser un número entero.")

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
                    setattr(libro, 'stock', stock)
                    agregar_libro(libro)
                    print("✅ Libro agregado correctamente.")
                except Exception as e:
                    print(f"Error: {e}")
                prompt_enter()

            case '3':
                try:
                    libros = listar_libros()
                    if not libros:
                        print("❌ No hay libros registrados para modificar.")
                        prompt_enter()
                        continue

                    print("\n--- Libros Disponibles ---")
                    headers = ["ID", "Título", "Autor",
                               "Categoría", "Año", "Stock"]
                    rows = []
                    for libro_item in libros:
                        cat_id = libro_item.categoria
                        cat = buscar_categoria_por_id(cat_id)
                        cat_nombre = cat['nombre'] if cat else cat_id

                        rows.append([
                            libro_item.id,
                            libro_item.titulo,
                            str(libro_item.autor),
                            cat_nombre,
                            libro_item.anio,
                            getattr(libro_item, 'stock', 0)
                        ])
                    print_table(headers, rows)
                    print()

                    id_libro = pedir_id_existente(lambda x: buscar_libro_por_id(x),
                                                  "ID del libro a modificar: ")
                    libro = buscar_libro_por_id(id_libro)
                    if not libro:
                        print("Libro no encontrado.")
                        continue
                    print("Deje en blanco para mantener el valor actual.")
                    nuevo_titulo = input(
                        f"Nuevo título [{libro['titulo']}]: ").strip() or libro['titulo']

                    cat_id_actual = libro['categoria']
                    cat_actual = buscar_categoria_por_id(cat_id_actual)
                    cat_nombre_actual = cat_actual['nombre'] if cat_actual else cat_id_actual

                    cambiar_categoria = input(
                        f"¿Desea cambiar la categoría actual '{cat_nombre_actual}'? (s/n): ").strip().lower()
                    if cambiar_categoria == 's':
                        nuevo_categoria = mostrar_menu_seleccion_categoria()
                        if not nuevo_categoria:
                            nuevo_categoria = libro['categoria']
                    else:
                        nuevo_categoria = libro['categoria']

                    nuevo_anio_input = input(
                        f"Nuevo año [{libro['anio']}]: ").strip()
                    nuevo_anio = int(
                        nuevo_anio_input) if nuevo_anio_input else libro['anio']
                    nuevo_stock_input = input(
                        f"Nuevo stock [{libro.get('stock', 0)}]: ").strip()
                    if nuevo_stock_input:
                        try:
                            nuevo_stock = int(nuevo_stock_input)
                            if nuevo_stock < 0:
                                print("❌ El stock no puede ser negativo.")
                                prompt_enter()
                                continue
                        except ValueError:
                            print("❌ El stock debe ser un número entero.")
                            prompt_enter()
                            continue
                    else:
                        nuevo_stock = libro.get('stock', 0)
                    nuevos_datos = {
                        'titulo': nuevo_titulo,
                        'categoria': nuevo_categoria,
                        'anio': int(nuevo_anio),
                        'stock': int(nuevo_stock)
                    }
                    modificar_libro(id_libro, nuevos_datos)
                    print("Libro modificado correctamente.")
                except Exception as e:
                    print(f"Error: {e}")
                prompt_enter()

            case '4':
                try:
                    libros = listar_libros()
                    if not libros:
                        print("❌ No hay libros registrados para eliminar.")
                        prompt_enter()
                        continue

                    print("\n--- Libros Disponibles ---")
                    headers = ["ID", "Título", "Autor",
                               "Categoría", "Año", "Stock"]
                    rows = []
                    for libro_item in libros:
                        cat_id = libro_item.categoria
                        cat = buscar_categoria_por_id(cat_id)
                        cat_nombre = cat['nombre'] if cat else cat_id

                        rows.append([
                            libro_item.id,
                            libro_item.titulo,
                            str(libro_item.autor),
                            cat_nombre,
                            libro_item.anio,
                            getattr(libro_item, 'stock', 0)
                        ])
                    print_table(headers, rows)
                    print()

                    id_libro = pedir_id_existente(lambda x: buscar_libro_por_id(x),
                                                  "ID del libro a eliminar: ")
                    eliminar_libro(id_libro)
                    print("✅ Libro eliminado correctamente.")
                except Exception as e:
                    print(f"❌ Error: {e}")
                prompt_enter()
            case '5':
                break
            case _:
                print("Opción no válida.")
                prompt_enter()


def menu_categorias():
    while True:
        print("\n--- GESTIÓN DE CATEGORÍAS ---")
        print("1. Listar categorías")
        print("2. Agregar categoría")
        print("3. Modificar categoría")
        print("4. Eliminar categoría")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        match opcion:
            case '1':
                categorias = listar_categorias()
                if not categorias:
                    print("❌ No hay categorías registradas.")
                else:
                    headers = ["ID", "Nombre", "Descripción"]
                    rows = [
                        [cat['id_categoria'], cat['nombre'],
                            cat.get('descripcion', '')]
                        for cat in categorias
                    ]
                    print("\n------------- LISTA DE CATEGORÍAS -------------\n")
                    print_table(headers, rows)
                prompt_enter()

            case '2':
                try:
                    print("\n--- Agregar Nueva Categoría ---")
                    nombre = input("Nombre de la categoría: ").strip()

                    if not nombre:
                        print("❌ El nombre no puede estar vacío.")
                        prompt_enter()
                        continue

                    if len(nombre) < 2:
                        print("❌ El nombre debe tener al menos 2 caracteres.")
                        prompt_enter()
                        continue

                    if buscar_categoria_por_nombre(nombre):
                        print(f"❌ Ya existe una categoría llamada '{nombre}'.")
                        prompt_enter()
                        continue

                    descripcion = input("Descripción (opcional): ").strip()

                    nueva_cat = agregar_categoria(nombre, descripcion)
                    print(
                        f"✅ Categoría '{nueva_cat['nombre']}' agregada correctamente con ID {nueva_cat['id_categoria']}.")

                except Exception as e:
                    print(f"❌ Error: {e}")
                prompt_enter()

            case '3':
                try:
                    categorias = listar_categorias()
                    if not categorias:
                        print("❌ No hay categorías para modificar.")
                        prompt_enter()
                        continue

                    print("\n--- Categorías Disponibles ---")
                    for idx, cat in enumerate(categorias, 1):
                        print(
                            f"{idx}. {cat['nombre']} (ID: {cat['id_categoria']})")

                    id_cat = input(
                        "\nIngrese el ID de la categoría a modificar: ").strip().upper()
                    categoria = buscar_categoria_por_id(id_cat)

                    if not categoria:
                        print("❌ Categoría no encontrada.")
                        prompt_enter()
                        continue

                    print(f"\nModificando: {categoria['nombre']}")
                    print("Deje en blanco para mantener el valor actual.")

                    nuevo_nombre = input(
                        f"Nuevo nombre [{categoria['nombre']}]: ").strip()
                    nueva_descripcion = input(
                        f"Nueva descripción [{categoria.get('descripcion', '')}]: ").strip()

                    if not nuevo_nombre:
                        nuevo_nombre = None

                    if not nueva_descripcion:
                        nueva_descripcion = None

                    modificar_categoria(
                        id_cat, nuevo_nombre, nueva_descripcion)
                    print("✅ Categoría modificada correctamente.")

                except ValueError as e:
                    print(f"❌ {e}")
                except Exception as e:
                    print(f"❌ Error: {e}")
                prompt_enter()

            case '4':
                try:
                    categorias = listar_categorias()
                    if not categorias:
                        print("❌ No hay categorías para eliminar.")
                        prompt_enter()
                        continue

                    print("\n--- Categorías Disponibles ---")
                    for idx, cat in enumerate(categorias, 1):
                        print(
                            f"{idx}. {cat['nombre']} (ID: {cat['id_categoria']})")

                    id_cat = input(
                        "\nIngrese el ID de la categoría a eliminar: ").strip().upper()
                    categoria = buscar_categoria_por_id(id_cat)

                    if not categoria:
                        print("❌ Categoría no encontrada.")
                        prompt_enter()
                        continue

                    confirmacion = input(
                        f"¿Está seguro de eliminar '{categoria['nombre']}'? (s/n): ").strip().lower()
                    if confirmacion == 's':
                        eliminar_categoria(id_cat)
                        print("✅ Categoría eliminada correctamente.")
                    else:
                        print("❌ Operación cancelada.")

                except ValueError as e:
                    print(f"❌ {e}")
                except Exception as e:
                    print(f"❌ Error: {e}")
                prompt_enter()

            case '5':
                break

            case _:
                print("❌ Opción no válida.")
                prompt_enter()


def menu_principal():
    while True:
        print("\n=== Sistema de Biblioteca ===")
        print("1. Gestión de libros")
        print("2. Gestión de miembros")
        print("3. Gestión de préstamos")
        print("4. Gestión de categorías")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")
        match opcion:
            case '1':
                menu_libros()
            case '2':
                menu_miembros()
            case '3':
                menu_prestamos()
            case '4':
                menu_categorias()
            case '5':
                confirmar_salida()
            case _:
                print("Opción no válida.")


if __name__ == "__main__":
    menu_principal()
