from matplotlib import pyplot as plt  
import math      
import numpy as np



class Calentador:
    def __init__(self, temperatura_inicial_agua , temperatura_final, temperatura_ambiente,resistencia = None, tension = None):
        self.temperatura_interior = temperatura_inicial_agua
        self.temperatura_final = temperatura_final
        self.temperatura_ambiente = temperatura_ambiente
        self.resistencia = resistencia
        self.tiempo = 210
        if tension:
            self.tension = tension
        else:
            self.tension = 220
        self.capacidad_recipiente = 1800
        self.capacidad_calorifica = 4186 # J/kg°C
        self.altura = 30 #cm 
        self.radio = 7 #cm
        self.espesor = 0.001 # 1 mm de espesor expresado en m
        self.k = 0.04  # Conductividad térmica de la fibra de vidrio

    def especificaciones(self):
        if self.resistencia:
            p = self.tension**2/self.resistencia  
            print(f'La resistencia es R: {self.resistencia}, la potencia {p}, la I {p/self.tension}')
        else:
            q = self.capacidad_recipiente * (self.capacidad_calorifica/1000) * (self.temperatura_final - self.temperatura_interior)# Energía calorífica
            p = q / self.tiempo #Potencia
            i = p / self.tension #Corriente 
            r = self.tension / i #Resistencia
            print(f'La resistencia es R: {r}, Q: {q}, la potencia {p}, la I {i}')
        self.aumento_por_segundo = p / (self.capacidad_recipiente * (self.capacidad_calorifica/1000)) #Aumento de temperatura por segundo

    def calentar(self, grafica_general=None):
        self.especificaciones()
        grafica_eje_x = []
        grafica_eje_y_sin_perdida = []
        grafica_eje_y_con_perdida = []
        temperatura_actual = self.temperatura_interior
        
        temperatura_ambiente_sin_evento = self.temperatura_ambiente
        estado_evento = 0
        fin_evento = 0
        superficie = (2 * math.pi * (self.radio**2) + 2 * math.pi * self.radio* self.altura)/10000 # m² - Se divide para pasarlo a m²
        segundo = 1
        while temperatura_actual < self.temperatura_final:
            rand = np.random.randint(1, 30)
            if rand == 1: # Ocurrencia del fenómeno estocástico
                print("estado evento: OCURRE EVENTO")
                if estado_evento == 0:
                    temperatura_ambiente_evento = temperatura_ambiente_sin_evento + np.random.randint(-50, 0) # Se elige una variación aleatoria en el rango [-50, 0] grados
                    duracion_descenso = np.random.randint(60, 120) # Se elige una duración aleatoria en el rango [10, 30] segundos
                    fin_evento = segundo + duracion_descenso
                    if fin_evento > self.tiempo:
                        fin_evento = self.tiempo
                    estado_evento = 1
                else:
                    pass

            if estado_evento == 1:
                if segundo == fin_evento:
                    estado_evento = 0
                else:
                    calor_perdido = self.k*superficie*(temperatura_actual - temperatura_ambiente_evento)/self.espesor #  W/K Calor perdido
                    print(f"Evento estocástico: {self.temperatura_ambiente} °C en el segundo {segundo}")
            elif estado_evento == 0:
                calor_perdido = self.k*superficie*(temperatura_actual - self.temperatura_ambiente)/self.espesor

            variacion_temperatura = self.aumento_por_segundo - (calor_perdido/self.capacidad_calorifica)
            print("La variacion de temperatura es de ", variacion_temperatura)
            grafica_eje_y_con_perdida.append(temperatura_actual)
            grafica_eje_x.append(segundo)
            temperatura_actual += variacion_temperatura
            segundo += 1

        if grafica_general:
            grafica_general.almacenar_datos(grafica_eje_x, grafica_eje_y_sin_perdida, grafica_eje_y_con_perdida,
            self.temperatura_final, self.tiempo)
        return f"La temperatura final del agua es de {temperatura_actual} °C en {segundo} segundos"

class Graficador:
    def __init__(self):
        self.graficas_eje_x = []
        self.graficas_eje_y_con_perdida = []
        self.temperatura_final = []
        self.tiempo = []

    def almacenar_datos(self, eje_x, eje_y_sin_perdida, eje_y_con_perdida, temperatura_final, segundos):
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
        
        tiempo = len(self.graficas_eje_x[0])
        if tiempo < 200 :
            intervalo = 15
        elif 199 < tiempo < 300:
            intervalo = 30
        elif tiempo > 299:
            intervalo = 50
        plt.xticks(range(0, tiempo + 1, intervalo))
        plt.show()

def main():
    #Los parametros que puedo variar son temperatura_interior, temperatura_que_quiere_llegar, temperatura_ambiente, resistencia y tension
    grafica_general = Graficador()

    temp_inicial_agua_dist_norm = np.random.normal(10, 5)    
    temp_ambiente = np.random.uniform(5, 30)   
    tension_dist_norm = np.random.normal(220, 40)
    
    calentador = Calentador(temp_inicial_agua_dist_norm, 100, temp_ambiente, 15, tension_dist_norm)
    calentador.calentar(grafica_general)

    decision = input('\nPresione enter para salir\n\n1 para grafico del fenómeno estocástico: ')
    if decision == '1':
        grafica_general.grafico_con_perdida()
    else: 
        pass

if __name__ == "__main__":
    main()