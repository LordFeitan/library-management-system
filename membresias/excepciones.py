# excepciones.py - EXCEPCIONES PARA ERRORES DEL SISTEMA

class ErrorBiblioteca(Exception):
    """Clase base para todas las excepciones de la biblioteca"""
    pass

# 🔥 EXCEPCIONES PARA SITUACIONES QUE NO SON DE VALIDACIÓN
class MiembroNoEncontradoError(ErrorBiblioteca):
    """Cuando se busca un miembro que no existe"""
    pass

class LibroNoEncontradoError(ErrorBiblioteca):
    """Cuando se busca un libro que no existe"""
    pass

class LibroNoDisponibleError(ErrorBiblioteca):
    """Cuando un libro no está disponible para préstamo"""
    pass

class IDDuplicadoError(ErrorBiblioteca):
    """Cuando se intenta crear un miembro con ID existente"""
    pass

class PrestamoActivoError(ErrorBiblioteca):
    """Cuando un libro ya está prestado"""
    pass

class ArchivoNoEncontradoError(ErrorBiblioteca):
    """Cuando no se puede encontrar un archivo JSON"""
    pass