from math import gamma, pi, sqrt


class RegresionLineal:
    def __init__(self, x, y):
        if len(x) != len(y):
            raise ValueError("X y Y deben tener la misma cantidad de datos.")
        if len(x) < 3:
            raise ValueError("Se necesitan al menos tres pares de datos.")

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
            (self.n * suma_x2 - suma_x ** 2) * (self.n * suma_y2 - suma_y ** 2),
            "No se puede calcular r con esos datos.",
        )
        return (self.n * suma_xy - suma_x * suma_y) / sqrt(denominador)

    def calcular_r2(self):
        return self.calcular_r() ** 2

    def predecir(self, xk):
        return self.calcular_b0() + self.calcular_b1() * xk

    def promedio_x(self):
        return sum(self.x) / self.n

    def suma_cuadrados_x(self):
        promedio = self.promedio_x()
        return sum((xi - promedio) ** 2 for xi in self.x)

    def sigma(self):
        b0 = self.calcular_b0()
        b1 = self.calcular_b1()
        suma = sum((self.y[i] - b0 - b1 * self.x[i]) ** 2 for i in range(self.n))
        return sqrt(suma / (self.n - 2))


class SimpsonTStudent:
    def __init__(self, dof, segmentos_iniciales=10, error=0.000001):
        if dof <= 0:
            raise ValueError("Los grados de libertad deben ser mayores que cero.")
        self.dof = dof
        self.segmentos_iniciales = segmentos_iniciales
        self.error = error

    def densidad(self, t):
        numerador = gamma((self.dof + 1) / 2)
        denominador = sqrt(self.dof * pi) * gamma(self.dof / 2)
        base = 1 + (t ** 2) / self.dof
        return (numerador / denominador) * (base ** (-(self.dof + 1) / 2))

    def calcular(self, x, n):
        ancho = x / n
        suma = self.densidad(0) + self.densidad(x)

        for i in range(1, n):
            t = i * ancho
            coeficiente = 4 if i % 2 != 0 else 2
            suma += coeficiente * self.densidad(t)

        return (ancho / 3) * suma

    def integrar(self, x):
        n = self.segmentos_iniciales

        while True:
            anterior = self.calcular(x, n)
            actual = self.calcular(x, n * 2)

            if abs(actual - anterior) < self.error:
                return actual

            n *= 2


class IntegracionInversa:
    def __init__(self, p, dof, tolerancia=0.00001):
        self.p = p
        self.tolerancia = tolerancia
        self.simpson = SimpsonTStudent(dof, error=tolerancia / 10)

    def calcular_x(self):
        x = 1.0
        d = 0.5
        error_anterior = None

        for _ in range(200):
            p_calculada = self.simpson.integrar(x)
            error_actual = self.p - p_calculada

            if abs(error_actual) < self.tolerancia:
                return x

            if error_anterior is not None and error_anterior * error_actual < 0:
                d /= 2

            if p_calculada < self.p:
                x += d
            else:
                x -= d

            error_anterior = error_actual

        raise ValueError("No se encontro el valor de t con la tolerancia indicada.")


class RangoPrediccion:
    def __init__(self, x, y, xk, p=0.35, tolerancia=0.00001):
        if p <= 0 or p >= 0.5:
            raise ValueError("p debe ser mayor que 0 y menor que 0.5.")

        self.regresion = RegresionLineal(x, y)
        self.xk = xk
        self.p = p
        self.tolerancia = tolerancia

    def calcular(self):
        n = self.regresion.n
        dof = n - 2
        b0 = self.regresion.calcular_b0()
        b1 = self.regresion.calcular_b1()
        r = self.regresion.calcular_r()
        r2 = self.regresion.calcular_r2()
        yk = self.regresion.predecir(self.xk)
        t = IntegracionInversa(self.p, dof, self.tolerancia).calcular_x()
        sigma = self.regresion.sigma()
        suma_cuadrados_x = self.regresion.suma_cuadrados_x()

        if suma_cuadrados_x == 0:
            raise ValueError("No se puede calcular el rango con esos valores de X.")

        factor = sqrt(1 + (1 / n) + (((self.xk - self.regresion.promedio_x()) ** 2) / suma_cuadrados_x))
        rango = t * sigma * factor

        return {
            "n": n,
            "dof": dof,
            "b0": b0,
            "b1": b1,
            "r": r,
            "r2": r2,
            "yk": yk,
            "t": t,
            "sigma": sigma,
            "rango": rango,
            "upi": yk + rango,
            "lpi": yk - rango,
            "significancia": 1 - 2 * self.p,
        }
