from datos.json_manager import cargar_datos, guardar_datos

RUTA_JSON_CATEGORIAS = 'datos/categorias.json'


def generar_siguiente_id_categoria():
    """Genera el siguiente ID de categoría automáticamente (CAT001, CAT002, ...)"""
    categorias = cargar_datos(RUTA_JSON_CATEGORIAS)
    if not categorias:
        return 'CAT001'

    numeros = []
    for categoria in categorias:
        id_str = categoria['id_categoria']
        if id_str.startswith('CAT') and len(id_str) > 3:
            try:
                numeros.append(int(id_str[3:]))
            except ValueError:
                continue

    if not numeros:
        return 'CAT001'

    siguiente_numero = max(numeros) + 1
    return f'CAT{siguiente_numero:03d}'


def listar_categorias():
    """Lista todas las categorías disponibles"""
    return cargar_datos(RUTA_JSON_CATEGORIAS)


def buscar_categoria_por_id(id_categoria):
    """Busca una categoría por su ID"""
    categorias = cargar_datos(RUTA_JSON_CATEGORIAS)
    for cat in categorias:
        if cat['id_categoria'] == id_categoria:
            return cat
    return None


def buscar_categoria_por_nombre(nombre):
    """Busca una categoría por su nombre (case-insensitive)"""
    categorias = cargar_datos(RUTA_JSON_CATEGORIAS)
    nombre_lower = nombre.lower().strip()
    for cat in categorias:
        if cat['nombre'].lower() == nombre_lower:
            return cat
    return None


def agregar_categoria(nombre, descripcion=""):
    """Agrega una nueva categoría"""
    categorias = cargar_datos(RUTA_JSON_CATEGORIAS)

    if buscar_categoria_por_nombre(nombre):
        raise ValueError(f"Ya existe una categoría con el nombre '{nombre}'.")

    id_categoria = generar_siguiente_id_categoria()

    nueva_categoria = {
        'id_categoria': id_categoria,
        'nombre': nombre.strip(),
        'descripcion': descripcion.strip()
    }

    categorias.append(nueva_categoria)
    guardar_datos(RUTA_JSON_CATEGORIAS, categorias)
    return nueva_categoria


def modificar_categoria(id_categoria, nuevo_nombre=None, nueva_descripcion=None):
    """Modifica una categoría existente"""
    categorias = cargar_datos(RUTA_JSON_CATEGORIAS)

    categoria_encontrada = False
    for cat in categorias:
        if cat['id_categoria'] == id_categoria:
            categoria_encontrada = True

            if nuevo_nombre and nuevo_nombre.strip() != cat['nombre']:
                if buscar_categoria_por_nombre(nuevo_nombre):
                    raise ValueError(
                        f"Ya existe una categoría con el nombre '{nuevo_nombre}'.")
                cat['nombre'] = nuevo_nombre.strip()

            if nueva_descripcion is not None:
                cat['descripcion'] = nueva_descripcion.strip()

            break

    if not categoria_encontrada:
        raise ValueError(
            f"No se encontró la categoría con ID '{id_categoria}'.")

    guardar_datos(RUTA_JSON_CATEGORIAS, categorias)


def eliminar_categoria(id_categoria):
    """Elimina una categoría"""
    from libros.gestion_libros import listar_libros

    libros = listar_libros()
    categoria = buscar_categoria_por_id(id_categoria)

    if categoria:
        libros_con_categoria = [
            l for l in libros if l.categoria == id_categoria]
        if libros_con_categoria:
            raise ValueError(
                f"No se puede eliminar la categoría porque hay {len(libros_con_categoria)} libro(s) asociado(s).")

    categorias = cargar_datos(RUTA_JSON_CATEGORIAS)
    categorias_filtradas = [
        cat for cat in categorias if cat['id_categoria'] != id_categoria]

    if len(categorias_filtradas) == len(categorias):
        raise ValueError(
            f"No se encontró la categoría con ID '{id_categoria}'.")

    guardar_datos(RUTA_JSON_CATEGORIAS, categorias_filtradas)


def mostrar_menu_seleccion_categoria():
    """
    Muestra un menú para seleccionar una categoría y retorna el ID seleccionado.
    También permite agregar una nueva categoría si no existe.
    """
    categorias = listar_categorias()

    print("\n" + "="*50)
    print("       SELECCIONE UNA CATEGORÍA")
    print("="*50)

    for idx, cat in enumerate(categorias, 1):
        print(f"{idx}. {cat['nombre']}")
        if cat.get('descripcion'):
            print(f"   └─ {cat['descripcion']}")

    print(f"\n{len(categorias) + 1}. ➕ Agregar nueva categoría")
    print("0. ❌ Cancelar")
    print("="*50)

    while True:
        try:
            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == '0':
                return None

            opcion_num = int(opcion)

            if 1 <= opcion_num <= len(categorias):
                return categorias[opcion_num - 1]['id_categoria']

            elif opcion_num == len(categorias) + 1:
                print("\n--- Nueva Categoría ---")
                nombre = input("Nombre de la categoría: ").strip()

                if not nombre:
                    print("❌ El nombre no puede estar vacío.")
                    continue

                if len(nombre) < 2:
                    print("❌ El nombre debe tener al menos 2 caracteres.")
                    continue

                if buscar_categoria_por_nombre(nombre):
                    print(f"❌ Ya existe una categoría llamada '{nombre}'.")
                    continue

                descripcion = input("Descripción (opcional): ").strip()

                try:
                    nueva_cat = agregar_categoria(nombre, descripcion)
                    print(
                        f"✅ Categoría '{nueva_cat['nombre']}' agregada correctamente.")
                    return nueva_cat['id_categoria']  # RETORNA ID
                except Exception as e:
                    print(f"❌ Error al agregar categoría: {e}")
                    continue
            else:
                print("❌ Opción no válida.")

        except ValueError:
            print("❌ Por favor ingrese un número válido.")
        except KeyboardInterrupt:
            print("\n\n❌ Operación cancelada.")
            return None
