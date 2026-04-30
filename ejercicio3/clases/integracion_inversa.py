from math import gamma, pi, sqrt


class DistribucionTStudent:
    def __init__(self, dof):
        if dof <= 0:
            raise ValueError("Los grados de libertad deben ser mayores que cero.")
        self.dof = dof

    def densidad(self, t):
        numerador = gamma((self.dof + 1) / 2)
        denominador = sqrt(self.dof * pi) * gamma(self.dof / 2)
        base = 1 + (t ** 2) / self.dof
        return (numerador / denominador) * (base ** (-(self.dof + 1) / 2))


class SimpsonTStudent:
    def __init__(self, dof, segmentos_iniciales=10, error=0.00001):
        if segmentos_iniciales <= 0 or segmentos_iniciales % 2 != 0:
            raise ValueError("Los segmentos iniciales deben ser un numero par y positivo.")
        if error <= 0:
            raise ValueError("El error aceptable debe ser mayor que cero.")

        self.distribucion = DistribucionTStudent(dof)
        self.segmentos_iniciales = segmentos_iniciales
        self.error = error

    def calcular(self, x, n):
        if n <= 0 or n % 2 != 0:
            raise ValueError("El numero de segmentos debe ser positivo y par.")

        if x == 0:
            return 0.0

        signo = 1 if x > 0 else -1
        limite = abs(x)
        ancho = limite / n
        suma = self.distribucion.densidad(0) + self.distribucion.densidad(limite)

        for i in range(1, n):
            t = i * ancho
            coeficiente = 4 if i % 2 != 0 else 2
            suma += coeficiente * self.distribucion.densidad(t)

        return signo * (ancho / 3) * suma

    def integrar(self, x):
        n = self.segmentos_iniciales

        while True:
            resultado_anterior = self.calcular(x, n)
            resultado_actual = self.calcular(x, n * 2)

            if abs(resultado_actual - resultado_anterior) < self.error:
                return resultado_actual, n * 2

            n *= 2


class IntegracionInversa:
    def __init__(self, p, dof, tolerancia=0.00001, d_inicial=0.5):
        if p <= 0 or p >= 0.5:
            raise ValueError("p debe ser mayor que 0 y menor que 0.5.")
        if tolerancia <= 0:
            raise ValueError("La tolerancia debe ser mayor que cero.")
        if d_inicial <= 0:
            raise ValueError("El valor inicial de d debe ser mayor que cero.")

        self.p = p
        self.tolerancia = tolerancia
        self.d_inicial = d_inicial
        self.simpson = SimpsonTStudent(dof, error=tolerancia / 1000)

    def calcular(self, max_iteraciones=200):
        bajo = 0.0
        alto = self.d_inicial
        iteraciones = []

        while self.simpson.integrar(alto)[0] < self.p:
            bajo = alto
            alto *= 2

        for numero_iteracion in range(1, max_iteraciones + 1):
            x = (bajo + alto) / 2
            p_calculada, segmentos = self.simpson.integrar(x)
            error_signo = self.p - p_calculada
            error_sin_signo = abs(error_signo)
            d = (alto - bajo) / 2

            iteraciones.append(
                {
                    "iteracion": numero_iteracion,
                    "x": x,
                    "p_calculada": p_calculada,
                    "error_signo": error_signo,
                    "error_sin_signo": error_sin_signo,
                    "d": d,
                    "segmentos": segmentos,
                }
            )

            if error_sin_signo < self.tolerancia and d < self.tolerancia / 10:
                return x, p_calculada, error_sin_signo, numero_iteracion, iteraciones

            if p_calculada < self.p:
                bajo = x
            else:
                alto = x

        raise ValueError("No se encontro una respuesta con la tolerancia indicada.")
