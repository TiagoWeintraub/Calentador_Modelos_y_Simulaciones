import random
from matplotlib import pyplot as plt  
import math      
import numpy as np

class Calentador:
    def __init__(self, temperatura_inicial_agua, temperatura_final, temperatura_ambiente, resistencia=None, tension=None):
        self.temperatura_inicial = temperatura_inicial_agua
        self.temperatura_final = temperatura_final
        self.temperatura_ambiente = temperatura_ambiente
        self.resistencia = resistencia
        self.tension = tension
        self.tiempo = 210
        self.capacidad_recipiente = 1800
        self.conductividad_fibra_de_vidrio = 0.04
        self.capacidad_calorifica = 4186  # J/kg°C
        self.altura = 30  # cm 
        self.radio = 7  # cm
        self.espesor = 0.001  # 1 mm de espesor expresado en m
        self.k = 0.04  # Conductividad térmica de la fibra de vidrio

    def especificaciones(self):
        if self.resistencia:
            p = self.tension**2 / self.resistencia  
            print(f'LA resistencia es R: {self.resistencia}, la potencia {p}, la I {p / self.tension}')
        else:
            q = self.capacidad_recipiente * (self.capacidad_calorifica / 1000) * (self.temperatura_final - self.temperatura_inicial)  # Energía calorífica
            p = q / self.tiempo  # Potencia
            i = p / self.tension  # Corriente 
            r = self.tension / i  # Resistencia
            print(f'LA resistencia es R: {r}, Q: {q}, la potencia {p}, la I {i}')
        self.aumento_por_segundo = p / (self.capacidad_recipiente * (self.capacidad_calorifica / 1000))  # Aumento de temperatura por segundo

    def calentar(self, grafica_general=None):
        self.especificaciones()
        grafica_eje_x = []
        grafica_eje_y_con_perdida = []
        temperatura_interior = self.temperatura_inicial
        temperatura_actual = self.temperatura_inicial
        superficie = (2 * math.pi * (self.radio**2) + 2 * math.pi * self.radio * self.altura) / 10000  # m² - Se divide para pasarlo a m²

        for segundo in range(self.tiempo):
            segundo_actual = segundo

            if random.randint(1, 300) == 1: # Ocurrencia del fenómeno estocástico
                descenso_grados = random.uniform(-50, 0) # Se elige una variación aleatoria en el rango [-50, 0] grados
                duracion_descenso = random.randint(1, 60) # Se elige una duración aleatoria en el rango [1, 60] segundos
                variacion_temperatura = descenso_grados / duracion_descenso # Para calcular cuantos grados baja por segundo
                for i in range(duracion_descenso):
                    grafica_eje_y_con_perdida.append(temperatura_actual)
                    grafica_eje_x.append(segundo_actual)
                    temperatura_actual += variacion_temperatura
            else:
                # Calor perdido debido a la diferencia de temperatura
                calor_perdido = self.k * superficie * (temperatura_actual - self.temperatura_ambiente) / self.espesor  # W/K Calor perdido
                variacion_temperatura = self.aumento_por_segundo - (calor_perdido / self.capacidad_calorifica)
                grafica_eje_y_con_perdida.append(temperatura_actual)
                grafica_eje_x.append(segundo_actual)
                temperatura_actual += variacion_temperatura

            temperatura_interior += self.aumento_por_segundo

        if grafica_general:
            grafica_general.almacenar_datos(grafica_eje_x, grafica_eje_y_con_perdida, self.temperatura_final, self.tiempo)
        return f"La temperatura final del agua es de {temperatura_actual} °C en {segundo_actual} segundos"

class Graficador:
    def __init__(self):
        self.graficas_eje_x = []
        self.graficas_eje_y_con_perdida = []
        self.temperatura_final = []
        self.tiempo = []

    def almacenar_datos(self, eje_x, eje_y_con_perdida, temperatura_final, segundos):
        self.graficas_eje_x.append(eje_x)
        self.graficas_eje_y_con_perdida.append(eje_y_con_perdida)
        self.temperatura_final.append(temperatura_final + 1)
        self.tiempo.append(segundos + 1)

    def grafico_con_perdida(self):
        for x, y in zip(self.graficas_eje_x, self.graficas_eje_y_con_perdida):
            plt.plot(x, y)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Temperatura del Líquido')
        max_temperatura_final = max(self.temperatura_final)
        plt.yticks(range(0, max_temperatura_final + 1, 5)) 
        max_tiempo = max(self.tiempo)
        plt.xticks(range(0, max_tiempo + 1, 15))
        plt.show()

def main():
    grafica_general = Graficador()
    
    resistencias_dist_unif = np.random.uniform(13, 25, 5)     # 5.A) CON 5 VALORES DISTINTOS DE RESISTENCIAS - DIST UNIFORME
    temp_inicial_agua_dist_norm = np.random.normal(10, 5, 5)    # 5.B) CON 5 VALORES DISTINTOS DE TEMP. INICIAL DEL AGUA - DIST NORMAL CON MEDIA 10 Y DESV. ESTANDAR 5
    temp_ambiente = np.random.uniform(-20, 50, 5)    # 5.C) CON 5 VALORES DISTINTOS DE TEMP. DEL AMBIENTE  - DIST NORMAL CON MEDIA 10 Y DESV. ESTANDAR 5
    tension_dist_norm = np.random.normal(220, 40, 5)     # 5.D) CON 5 VALORES DISTINTOS DE TENSION DE ALIMENTACION - DIST NORMAL CON MEDIA 12 Y DESV. ESTANDAR 4 - LUEGO DIST NORMAL CON MEDIA 220 Y DESV. ESTANDAR 40.
    
    for i in range(5):
        calentador = Calentador(temp_inicial_agua_dist_norm[i], 100, temp_ambiente[i], resistencias_dist_unif[i], tension_dist_norm[i])
        calentador.calentar(grafica_general)
        print("Resistencia: ", resistencias_dist_unif[i], "Temperatura inicial: ", temp_inicial_agua_dist_norm[i], "Temperatura ambiente: ", temp_ambiente[i], "Tension: ", tension_dist_norm[i])

    decision = input('\nPresione enter para salir\n\n1 para grafico CON perdida de calor: ')
    if decision == '1':
        grafica_general.grafico_con_perdida()
    else: 
        pass

if __name__ == "__main__":
    main()
