from abc import ABC, abstractmethod
from datetime import date, timedelta

class Penalizacion(ABC):
    """Clase abstracta para penalizaciones"""
    
    def __init__(self, prestamo, dias_retraso: int):
        self._prestamo = prestamo
        self._dias_retraso = dias_retraso
        self._fecha_aplicacion = date.today()
    
    @property
    def prestamo(self):
        return self._prestamo
    
    @property
    def dias_retraso(self):
        return self._dias_retraso
    
    @property
    def fecha_aplicacion(self):
        return self._fecha_aplicacion
    
    @abstractmethod
    def calcular_penalizacion(self) -> float:
        """Calcula el monto de la penalización"""
        pass
    
    @abstractmethod
    def aplicar_penalizacion(self):
        """Aplica la penalización al miembro"""
        pass
    
    @abstractmethod
    def get_descripcion(self) -> str:
        """Obtiene la descripción de la penalización"""
        pass

class PenalizacionMonetaria(Penalizacion):
    """Penalización monetaria por retraso"""
    
    def __init__(self, prestamo, dias_retraso: int, tarifa_por_dia: float = 1.0):
        super().__init__(prestamo, dias_retraso)
        self._tarifa_por_dia = tarifa_por_dia
    
    def calcular_penalizacion(self) -> float:
        return self._dias_retraso * self._tarifa_por_dia
    
    def aplicar_penalizacion(self):
        monto = self.calcular_penalizacion()
        # En un sistema real, aquí se registraría en la base de datos
        print(f"⚠️  Penalización aplicada: ${monto:.2f} por {self._dias_retraso} días de retraso")
        return monto
    
    def get_descripcion(self) -> str:
        return f"Multa por retraso: ${self.calcular_penalizacion():.2f}"

class PenalizacionSuspension(Penalizacion):
    """Penalización por suspensión de préstamos"""
    
    def __init__(self, prestamo, dias_retraso: int, dias_suspension_por_dia_retraso: int = 2):
        super().__init__(prestamo, dias_retraso)
        self._dias_suspension_por_dia_retraso = dias_suspension_por_dia_retraso
        self._dias_suspension = self._calcular_dias_suspension()
    
    def _calcular_dias_suspension(self) -> int:
        return self._dias_retraso * self._dias_suspension_por_dia_retraso
    
    def calcular_penalizacion(self) -> float:
        return 0.0  # No hay multa monetaria
    
    def aplicar_penalizacion(self):
        fecha_fin_suspension = date.today() + timedelta(days=self._dias_suspension)
        # En un sistema real, aquí se registraría la suspensión
        print(f" Miembro suspendido por {self._dias_suspension} días. Hasta: {fecha_fin_suspension}")
        return self._dias_suspension
    
    def get_descripcion(self) -> str:
        return f"Suspensión por {self._dias_suspension} días"

class PenalizacionCombinada(Penalizacion):
    """Penalización que combina multa y suspensión"""
    
    def __init__(self, prestamo, dias_retraso: int):
        super().__init__(prestamo, dias_retraso)
        self._penalizacion_monetaria = PenalizacionMonetaria(prestamo, dias_retraso)
        self._penalizacion_suspension = PenalizacionSuspension(prestamo, dias_retraso)
    
    def calcular_penalizacion(self) -> float:
        return self._penalizacion_monetaria.calcular_penalizacion()
    
    def aplicar_penalizacion(self):
        multa = self._penalizacion_monetaria.aplicar_penalizacion()
        suspension = self._penalizacion_suspension.aplicar_penalizacion()
        return {
            'multa': multa,
            'dias_suspension': suspension
        }
    
    def get_descripcion(self) -> str:
        return f"Multa: ${self.calcular_penalizacion():.2f} + Suspensión: {self._penalizacion_suspension._dias_suspension} días"