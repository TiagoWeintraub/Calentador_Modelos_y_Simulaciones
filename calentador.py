from matplotlib import pyplot as plt        

class Calentador:
    def __init__(self, nombre, temperatura_inicial , temperatura_final,  capacidad_calorifica, temperatura_entorno, segundos):
        self.temperatura_inicial = temperatura_inicial
        self.capacidad_calorifica = capacidad_calorifica
        self.nombre = nombre
        self.tiempo = segundos
        self.tension = 220
        self.capacidad_recipiente = 1.8
        self.conductividad_fibra_de_vidrio = 0.04
        self.temperatura_final = temperatura_final
        self.temperatura_entorno = temperatura_entorno
        self.aumento_por_segundo = 0
        self.grafica_eje_x = []
        self.grafica_eje_y_sin_perdida = []
        self.grafica_eje_y_con_perdida = []
        

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
        temperatura_actual_con_perdida = self.temperatura_actual
        for segundo in range(0,self.tiempo+1):
            segundo_actual = segundo
            self.grafica_eje_x.append(segundo_actual)
            self.grafica_eje_y_sin_perdida.append(temperatura_actual)
            self.grafica_eje_y_con_perdida.append(temperatura_actual_con_perdida)
            print(f"Segundo {segundo_actual}: {temperatura_actual} °C")
            temperatura_actual += self.aumento_por_segundo
        if grafica_general:
            grafica_general.almacenar_datos(self.grafica_eje_x, self.grafica_eje_y_sin_perdida, self.grafica_eje_y_con_perdida,self.nombre, self.temperatura_final, self.tiempo)
        return f"La temperatura del {self.nombre} final es de {temperatura_actual} °C en {segundo_actual} segundos"

class Graficar:
    def __init__(self):
        self.graficas_eje_x = []
        self.graficas_eje_y_sin_perdida = []
        self.graficas_eje_y_con_perdida = []
        self.nombres = []
        self.temperatura_final = []
        self.tiempo = []
    
    def almacenar_datos(self, eje_x, eje_y_sin_perdida, eje_y_con_perdida, nombre, temperatura_final, segundos):
        self.graficas_eje_x.append(eje_x)
        self.graficas_eje_y_sin_perdida.append(eje_y_sin_perdida)
        self.nombres.append(nombre)
        self.temperatura_final.append(temperatura_final + 1)
        self.tiempo.append(segundos + 1)
    
    def graficar_sin_perdida(self):
        for x, y, nombre in zip(self.graficas_eje_x, self.graficas_eje_y_sin_perdida, self.nombres):
            plt.plot(x, y, label=nombre)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Temperatura del Líquido')
        max_temperatura_final = max(self.temperatura_final)
        plt.yticks(range(0, max_temperatura_final + 1, 5)) 
        max_tiempo = max(self.tiempo)
        plt.xticks(range(0, max_tiempo + 1, 15))
        plt.legend()
        plt.show()
    
    def graficar_con_perdida(self):
        for x, y, nombre in zip(self.graficas_eje_x, self.graficas_eje_y_con_perdida, self.nombres):
            plt.plot(x, y, label=nombre)
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
# nombre, temperatura_inicial, temperatura_que_quiere_llegar, capacidad_calorifica, temperatura_entorno, segundos
    grafica_general = Graficar()
    
    calentador1 = Calentador("Agua", 15, 100, 4.186, 15, 210)
    calentador1.especificaciones()
    calentador1.calentar(grafica_general)
    
    calentador2 = Calentador("Agua", 20, 85, 4.186, 25, 210)
    calentador2.especificaciones()
    calentador2.calentar(grafica_general)

    grafica_general.graficar_sin_perdida()
    #grafica_general.graficar_con_perdida()