from matplotlib import pyplot as plt

class Liquidos:
    def __init__(self, nombre, temperatura_inicial, capacidad_calorifica):
        self.temperatura_inicial = temperatura_inicial
        self.capacidad_calorifica = capacidad_calorifica
        self.nombre = nombre

class Calentador(Liquidos):
    def __init__(self, nombre, temperatura_inicial , capacidad_calorifica, temperatura_entorno):
        super().__init__(nombre, temperatura_inicial, capacidad_calorifica)
        self.tiempo = 210
        self.tension = 220
        self.capacidad_recipiente = 1.8
        self.temperatura_final = 100
        self.temperatura_entorno = temperatura_entorno
        self.aumento_por_segundo = 0
        self.grafica_eje_x = []
        self.grafica_eje_y = []


    def especificaciones(self):
        # Energía calorífica
        Q = self.capacidad_recipiente * self.capacidad_calorifica * (self.temperatura_final - self.temperatura_inicial)
        #Potencia
        P = Q / self.tiempo
        #Corriente
        I = P / self.tension 
        #Resistencia
        R = self.tension / I
        #Aumento de temperatura por segundo
        self.aumento_por_segundo = P / (self.capacidad_recipiente * self.capacidad_calorifica)
        print(f"La potencia es de {P} W, la corriente es de {I} A, la resistencia es de {R} Ω y el aumento de temperatura por segundo es de {self.aumento_por_segundo} °C/s") 

    def calentar(self, grafica_general=None):
        temperatura_actual = self.temperatura_inicial
        for segundo in range(0,self.tiempo+1):
            segundo_actual = segundo
            self.grafica_eje_x.append(segundo_actual)
            self.grafica_eje_y.append(temperatura_actual)
            print(f"Segundo {segundo_actual}: {temperatura_actual} °C")
            temperatura_actual += self.aumento_por_segundo
        if grafica_general:
            grafica_general.almacenar_datos(self.grafica_eje_x, self.grafica_eje_y, self.nombre)
        return f"La temperatura del {self.nombre} final es de {temperatura_actual} °C en {segundo_actual} segundos"

class Graficar:
    def __init__(self):
        self.graficas_eje_x = []
        self.graficas_eje_y = []
        self.nombres = []
        self.temperatura_final = 100
    
    def almacenar_datos(self, eje_x, eje_y, nombre):
        self.graficas_eje_x.append(eje_x)
        self.graficas_eje_y.append(eje_y)
        self.nombres.append(nombre)
    
    def graficar(self):
        for x, y, nombre in zip(self.graficas_eje_x, self.graficas_eje_y, self.nombres):
            plt.plot(x, y, label=nombre)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Temperatura del Líquido')
        plt.yticks(range(0, self.temperatura_final + 1, 5))    
        plt.legend()    
        plt.show()


if __name__ == "__main__":
#temperatura_inicial, capacidad_calorifica, temperatura_entorno
    grafica_general = Graficar()
    
    calentador1 = Calentador("Agua", 15, 4.186, 15)
    calentador1.especificaciones()
    calentador1.calentar(grafica_general)
    
    calentador2 = Calentador("Agua2", 20, 4.186, 25)
    calentador2.especificaciones()
    calentador2.calentar(grafica_general)

    grafica_general.graficar()