from matplotlib import pyplot as plt  
import math      

class Calentador:
    def __init__(self, temperatura_inicial_agua , temperatura_final, temperatura_exterior):
        self.temperatura_interior = temperatura_inicial_agua
        self.tiempo = 210
        self.tension = 220
        self.capacidad_recipiente = 1800
        self.conductividad_fibra_de_vidrio = 0.04
        self.temperatura_final = temperatura_final
        self.temperatura_exterior = temperatura_exterior

    def especificaciones(self):
        capacidad_calorifica = 4.186
        Q = self.capacidad_recipiente * capacidad_calorifica * (self.temperatura_final - self.temperatura_interior)# Energía calorífica
        P = Q / self.tiempo #Potencia
        I = P / self.tension #Corriente 
        R = self.tension / I #Resistencia
        self.aumento_por_segundo = P / (self.capacidad_recipiente * capacidad_calorifica) #Aumento de temperatura por segundo


    def calentar(self, grafica_general=None):
        self.especificaciones()
        grafica_eje_x = []
        grafica_eje_y_sin_perdida = []
        grafica_eje_y_con_perdida = []
        temperatura_interior = self.temperatura_interior
        temperatura_actual = self.temperatura_interior
        temperatura_exterior = 15
        capacidad_calorifica = 4186 # J/kg°C
        altura = 30 #cm 
        radio = 7 #cm
        espesor = 0.001 # 2 mm de espesor expresado en m
        k = 0.04  # Conductividad térmica de la fibra de vidrio
        superficie = (2 * math.pi * (radio**2) + 2 * math.pi * radio* altura)/10000 # m² - Se divide para pasarlo a m²
        print(f"La superficie del recipiente es de {superficie} m²")
        densidad_agua = 994 # kg/m³

        for segundo in range(self.tiempo):
            segundo_actual = segundo

            calor_perdido = k*superficie*(temperatura_actual - temperatura_exterior)/espesor #  W/K Calor perdido
            variacion_temperatura = self.aumento_por_segundo - (calor_perdido/capacidad_calorifica)
            print(f"Segundo {segundo_actual}: {temperatura_actual} °C + suma rara {densidad_agua/capacidad_calorifica} -   restarara  {calor_perdido/capacidad_calorifica} W")
            grafica_eje_y_con_perdida.append(temperatura_actual)
            grafica_eje_x.append(segundo_actual)
            temperatura_actual += variacion_temperatura
            
            
            
            grafica_eje_y_sin_perdida.append(temperatura_interior)
            temperatura_interior += self.aumento_por_segundo
        print(grafica_eje_y_con_perdida)

        if grafica_general:
            grafica_general.almacenar_datos(grafica_eje_x, grafica_eje_y_sin_perdida, grafica_eje_y_con_perdida,
            self.temperatura_final, self.tiempo)
        return f"La temperatura final del agua es de {temperatura_actual} °C en {segundo_actual} segundos"


class Graficador:
    def __init__(self):
        self.graficas_eje_x = []
        self.graficas_eje_y_sin_perdida = []
        self.graficas_eje_y_con_perdida = []
        self.temperatura_final = []
        self.tiempo = []

    def almacenar_datos(self, eje_x, eje_y_sin_perdida, eje_y_con_perdida, temperatura_final, segundos):
        self.graficas_eje_x.append(eje_x)
        self.graficas_eje_y_sin_perdida.append(eje_y_sin_perdida)
        self.graficas_eje_y_con_perdida.append(eje_y_con_perdida)
        self.temperatura_final.append(temperatura_final + 1)
        self.tiempo.append(segundos + 1)

    def grafico_sin_perdida(self):
        for x, y in zip(self.graficas_eje_x, self.graficas_eje_y_sin_perdida):
            plt.plot(x, y)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Temperatura del Líquido')
        max_temperatura_final = max(self.temperatura_final)
        plt.yticks(range(0, max_temperatura_final + 1, 5)) 
        max_tiempo = max(self.tiempo)
        plt.xticks(range(0, max_tiempo + 1, 15))
        plt.show()

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


if __name__ == "__main__":
#Los parametros que puedo variar son temperatura_interior, temperatura_que_quiere_llegar, temperatura_exterior
    grafica_general = Graficador()
    
    calentador1 = Calentador( 15, 100, 15)
    calentador1.especificaciones()
    calentador1.calentar(grafica_general)
    
    calentador2 = Calentador(20, 100, 25)
    calentador2.especificaciones()
    calentador2.calentar(grafica_general)
    
    calentador3 = Calentador(10, 100, 25)
    calentador3.especificaciones()
    calentador3.calentar(grafica_general)
    
    calentador4 = Calentador(5, 100, 0)
    calentador4.especificaciones()
    calentador4.calentar(grafica_general)

    def main():
        decision = input('1 para grafico SIN perdida de calor \n2 para grafico CON perdida de calor: ')
        if decision == '1':
            grafica_general.grafico_sin_perdida()
        elif decision == '2':
            grafica_general.grafico_con_perdida()
    main()