from math import gamma, pi, sqrt


class IntegradorNumerico:
    def __init__(self, x, num_seg, error):
        self.x = x
        self.num_seg = num_seg
        self.error = error

    def funcion(self, t):
        """
        Método que deben implementar las clases hijas
        """
        raise NotImplementedError

    def calcular(self, n):
        """
        Método que deben implementar las clases hijas
        """
        raise NotImplementedError

    def integrar(self):
        n = self.num_seg

        while True:
            r1 = self.calcular(n)
            r2 = self.calcular(n * 2)

            if abs(r2 - r1) < self.error:
                return r2, n * 2

            n *= 2


class Simpson(IntegradorNumerico):
    def __init__(self, x, dof, num_seg, error):
        super().__init__(x, num_seg, error)
        self.dof = dof

    def funcion(self, t):
        numerador = gamma((self.dof + 1) / 2)
        denominador = sqrt(self.dof * pi) * gamma(self.dof / 2)
        base = 1 + (t ** 2) / self.dof

        return (numerador / denominador) * (base ** (-(self.dof + 1) / 2))

    def calcular(self, n):
        if n <= 0 or n % 2 != 0:
            raise ValueError("El numero de segmentos debe ser positivo y par.")

        w = self.x / n
        suma = self.funcion(0) + self.funcion(self.x)

        for i in range(1, n):
            t = i * w
            coeficiente = 4 if i % 2 != 0 else 2
            suma += coeficiente * self.funcion(t)

        return (w / 3) * suma
