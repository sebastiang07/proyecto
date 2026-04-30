# clases/regresion.py
import math


class RegresionLineal:
    def __init__(self, x, y):
        if len(x) != len(y):
            raise ValueError("X y Y deben tener la misma cantidad de datos.")
        if len(x) < 2:
            raise ValueError("Se necesitan al menos dos pares de datos.")

        self.x = x
        self.y = y
        self.n = len(x)

    def _validar_denominador(self, denominador, mensaje):
        if denominador == 0:
            raise ValueError(mensaje)
        return denominador

    def calcular_b1(self):
        suma_xy = sum(self.x[i] * self.y[i] for i in range(self.n))
        suma_x = sum(self.x)
        suma_y = sum(self.y)
        suma_x2 = sum(xi ** 2 for xi in self.x)
        denominador = self._validar_denominador(
            self.n * suma_x2 - suma_x ** 2,
            "No se puede calcular B1 con esos datos.",
        )
        return (self.n * suma_xy - suma_x * suma_y) / denominador

    def calcular_b0(self):
        return sum(self.y) / self.n - self.calcular_b1() * (sum(self.x) / self.n)

    def calcular_r(self):
        suma_xy = sum(self.x[i] * self.y[i] for i in range(self.n))
        suma_x = sum(self.x)
        suma_y = sum(self.y)
        suma_x2 = sum(xi ** 2 for xi in self.x)
        suma_y2 = sum(yi ** 2 for yi in self.y)
        denominador = self._validar_denominador(
            (self.n * suma_x2 - suma_x**2) *
            (self.n * suma_y2 - suma_y**2),
            "No se puede calcular r con esos datos.",
        )

        return (self.n * suma_xy - suma_x * suma_y) / math.sqrt(
            denominador
        )

    def calcular_r2(self):
        return self.calcular_r() ** 2

    def predecir(self, x):
        return self.calcular_b0() + self.calcular_b1() * x
