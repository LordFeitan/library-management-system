from libros.libro import Libro
from .miembro import Miembro
from datetime import date, timedelta

class Prestamo:
    DIAS_PRESTAMO = 14
    
    def __init__(self, id_prestamo: str, miembro: Miembro, libro: Libro, fecha_prestamo: date, fecha_devolucion: date = None):
        self._id_prestamo = id_prestamo.upper()
        self._miembro = miembro
        self._libro = libro
        self._fecha_prestamo = fecha_prestamo
        self._fecha_devolucion = fecha_devolucion

    @property
    def id_prestamo(self):
        return self._id_prestamo.upper()

    @property
    def miembro(self):
        return self._miembro

    @property
    def libro(self):
        return self._libro

    @property
    def fecha_prestamo(self):
        return self._fecha_prestamo

    @property
    def fecha_devolucion(self):
        return self._fecha_devolucion

    @fecha_devolucion.setter
    def fecha_devolucion(self, valor):
        self._fecha_devolucion = valor

    @property
    def fecha_limite(self):
        """Calcula la fecha límite para la devolución"""
        return self._fecha_prestamo + timedelta(days=self.DIAS_PRESTAMO)

    @property
    def dias_retraso(self):
        """Calcula los días de retraso (0 si no hay retraso)"""
        if self._fecha_devolucion:
            dias = (self._fecha_devolucion - self.fecha_limite).days
        else:
            dias = (date.today() - self.fecha_limite).days
        return max(0, dias)  # Retorna 0 si no hay retraso

    @property
    def esta_retrasado(self):
        """Verifica si el préstamo está retrasado"""
        return self.dias_retraso > 0

    def __str__(self):
        estado = f"(Devuelto)" if self.fecha_devolucion else f"(Pendiente - Vence: {self.fecha_limite})"
        if self.esta_retrasado:
            estado += f" ⚠️ RETRASADO {self.dias_retraso} días"
        return f"Préstamo {self.id_prestamo}: {self.libro.titulo} a {self.miembro.nombre} el {self.fecha_prestamo} {estado}"