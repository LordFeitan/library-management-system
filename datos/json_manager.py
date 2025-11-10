import json
import os


def cargar_datos(ruta):
    if not os.path.exists(ruta):
        return []
    with open(ruta, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def guardar_datos(ruta, datos):
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
