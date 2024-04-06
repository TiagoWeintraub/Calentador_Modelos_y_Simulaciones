from matplotlib import pyplot as plt  
import math      

class Calentador:
    def __init__(self, liquido, temperatura_inicial , temperatura_final, temperatura_entorno, segundos):
        self.temperatura_inicial = temperatura_inicial
        self.liquido = liquido
        self.tiempo = segundos
        self.tension = 220
        self.capacidad_recipiente = 1.8
        self.conductividad_fibra_de_vidrio = 0.04
        self.temperatura_final = temperatura_final
        self.temperatura_entorno = temperatura_entorno

    def especificaciones(self):
        self.capacidad_calorifica = 4.186
        Q = self.capacidad_recipiente * self.capacidad_calorifica * (self.temperatura_final - self.temperatura_inicial)# Energía calorífica
        P = Q / self.tiempo #Potencia
        I = P / self.tension #Corriente 
        R = self.tension / I #Resistencia
        self.aumento_por_segundo = P / (self.capacidad_recipiente * self.capacidad_calorifica) #Aumento de temperatura por segundo
        print(f"La potencia es de {P} W, la corriente es de {I} A, la resistencia es de {R} Ω y el aumento de temperatura por segundo es de {self.aumento_por_segundo} °C/s") 
        
    def calentar(self, grafica_general=None):
        self.especificaciones()
        grafica_eje_x = []
        grafica_eje_y_sin_perdida = []
        grafica_eje_y_con_perdida = []
        temperatura_actual = self.temperatura_inicial
        altura = 0.3 
        radio = 0.07
        espesor = 0.002
        k = 0.4 #Conductividad térmica de la fibra de vidrio
        densidad = 0.0012
        area_bases = 2*(radio**2)
        area_lateral = 2*math.pi*radio*altura
        area_superficial = area_bases + area_lateral
        calor_perdido = (k*area_superficial*(temperatura_actual - self.temperatura_entorno))/espesor
        #temp_act_perdida= temperatura_actual + (densidad/self.capacidad_calorifica)-(calor_perdido/self.capacidad_calorifica)

        for segundo in range(0,self.tiempo+1):
            segundo_actual = segundo
            grafica_eje_x.append(segundo_actual)
            grafica_eje_y_sin_perdida.append(temperatura_actual)
            temperatura_actual_con_perdida =temperatura_actual -calor_perdido 
            grafica_eje_y_con_perdida.append(temperatura_actual_con_perdida)
            print(f"Segundo {segundo_actual}: {temperatura_actual} °C")
            temperatura_actual += self.aumento_por_segundo
        if grafica_general:
            grafica_general.almacenar_datos(grafica_eje_x, grafica_eje_y_sin_perdida, grafica_eje_y_con_perdida,self.liquido, self.temperatura_final, self.tiempo)
        return f"La temperatura del {self.liquido} final es de {temperatura_actual} °C en {segundo_actual} segundos"

class Graficador:
    def __init__(self):
        self.graficas_eje_x = []
        self.graficas_eje_y_sin_perdida = []
        self.graficas_eje_y_con_perdida = []
        self.liquidos = []
        self.temperatura_final = []
        self.tiempo = []

    def almacenar_datos(self, eje_x, eje_y_sin_perdida, eje_y_con_perdida, liquido, temperatura_final, segundos):
        self.graficas_eje_x.append(eje_x)
        self.graficas_eje_y_sin_perdida.append(eje_y_sin_perdida)
        self.graficas_eje_y_con_perdida.append(eje_y_con_perdida)
        self.liquidos.append(liquido)
        self.temperatura_final.append(temperatura_final + 1)
        self.tiempo.append(segundos + 1)

    def grafico_sin_perdida(self):
        for x, y, liquido in zip(self.graficas_eje_x, self.graficas_eje_y_sin_perdida, self.liquidos):
            plt.plot(x, y, label=liquido)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Temperatura del Líquido')
        max_temperatura_final = max(self.temperatura_final)
        plt.yticks(range(0, max_temperatura_final + 1, 5)) 
        max_tiempo = max(self.tiempo)
        plt.xticks(range(0, max_tiempo + 1, 15))
        plt.legend()
        plt.show()

    def grafico_con_perdida(self):
        for x, y, liquido in zip(self.graficas_eje_x, self.graficas_eje_y_con_perdida, self.liquidos):
            plt.plot(x, y, label=liquido)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Temperatura del Líquido')
        max_temperatura_final = max(self.temperatura_final)
        plt.yticks(range(0, max_temperatura_final + 1, 5)) 
        max_tiempo = max(self.tiempo)
        plt.xticks(range(0, max_tiempo + 1, 15))
        plt.legend()
        plt.show()


if __name__ == "__main__":
# liquido, temperatura_inicial, temperatura_que_quiere_llegar, capacidad_calorifica, temperatura_entorno, segundos
    grafica_general = Graficador()
    
    calentador1 = Calentador("Agua", 15, 100, 15, 210)
    calentador1.especificaciones()
    calentador1.calentar(grafica_general)
    
    calentador2 = Calentador("Agua", 20, 85, 25, 210)
    calentador2.especificaciones()
    calentador2.calentar(grafica_general)

    #grafica_general.grafico_sin_perdida()
    grafica_general.grafico_con_perdida()
