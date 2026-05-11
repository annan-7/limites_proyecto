import matplotlib.pyplot as plt # para graficar
import numpy as np # para crear arrays de números eje x
import customtkinter as ctk # para la interfaz gráfica


functioninput= input("Ingrese su función: ") # FUNCION A EVALUAR
PUNTO_CRITICO = float(input("Ingrese el punto crítico de su función: ")) # PUNTO CRÍTICO A EVALUAR

def function(x):
    allowed = {
        "x": x, # SOLO SE PERMITE USAR LA VARIABLE X
        
    }
    return eval(functioninput, {"__builtins__": None}, allowed) 
    # SI EL FUNCIÓN NO ES VÁLIDA, SE LANZARÁ UNA EXCEPCIÓN, QUE SE MANEJARÁ MÁS ADELANTE

    

#clave: function(puntoCritico-0.001) == function(puntoCritico+0.001) 
LimiteExiste=False;

def LimitesLaterales(puntoCritico):
    aproximaciónes = [0.1, 0.01, 0.001, 0.0001] # PARA QUE TENGAMOS MAS PUNTOS DE EVALUACIÓN
    izquierda = [] # VALORES DE IZQUIERDA
    derecha = [] # VALORES DE DERECHA
    try: 
        for h in aproximaciónes:
            valorIzq = puntoCritico - h # EVALUAMOS DESDE LA IZQUIERDA
            valorDer = puntoCritico + h # EVALUAMOS DESDE LA DERECHA

            valorYIzq = function(valorIzq) # EVALUAMOS LA FUNCIÓN EN EL VALOR DE LA IZQUIERDA
            valorYDer = function(valorDer)  # EVALUAMOS LA FUNCIÓN EN EL VALOR DE LA DERECHA

            izquierda.append(valorYIzq) # APPEND PARA AGRGAR EL LA LISTA DE IZQUIERDA
            derecha.append(valorYDer) # APPEND PARA AGRGAR EL LA LISTA DE DERECHA
    except Exception: # SI HAY UNA EXCEPCIÓN, ASUMIMOS QUE LA FUNCIÓN SE VA A INFINITO
        print("No existe el límite, la función se va a infinito")
        return None, False
    epsilon = 1e-2  # El margen de error 1E-2 SIGNIFICA 0.01 MARGEN DE ERROR 
    ultimoIzq = izquierda[-1] # OBTENEMOS EL ÚLTIMO VALOR DE LA IZQUIERDA
    ultimoDer = derecha[-1] # OBTENEMOS EL ÚLTIMO VALOR DE LA DERECHA
    existe = abs(ultimoIzq - ultimoDer) < epsilon # CAMPARAMOS CON EL MARGEN DE ERROR PARA VER SI EXISTE EL LÍMITE
    limite = (ultimoIzq + ultimoDer) / 2 # PROMEDIO DE LOS DOS ÚLTIMOS VALORES PARA OBTENER EL LÍMITE APROXIMADO
    print(f"El límite lateral izquierdo es: {ultimoIzq}")
    print(f"El límite lateral derecho es: {ultimoDer}")
    print(f"El límite es: {limite}")
    return limite, existe
    
    




def continuidadDeFuncion(puntoCritico):
    try:
       fxis=function(puntoCritico) # EVALUAMOS LA FUNCIÓN EN EL PUNTO CRÍTICO PARA VER SI ESTÁ DEFINIDA
       definida = True
    except ZeroDivisionError: # EN EL CAOS DE DIVISIÓN POR CERO, ASUMIMOS QUE NO ESTÁ DEFINIDA
        definida = False

    limite, existe = LimitesLaterales(puntoCritico) # OBTENEMOS EL LÍMITE Y SI EXISTE

    if not existe :
        print(f"No existe el límite en el punto crítico: {puntoCritico}")
        return None
        
    
    # ABS = VALOR ABSOLUTO PARA COMPARAR EL VALOR DE LA FUNCIÓN EN EL PUNTO CRÍTICO CON EL LÍMITE, 
    # SI SON IGUALES DENTRO DEL MARGEN DE ERROR, LA FUNCIÓN ES CONTINUA
    
    if(definida and (abs(fxis - limite) < 1e-2)): # QUE ESTE DEFINIDA Y QUE EL VALOR DE LA FUNCIÓN EN EL PUNTO CRÍTICO SEA IGUAL AL LÍMITE DENTRO DEL MARGEN DE ERROR
        print(f"La función es continua en el punto: {puntoCritico}")
    else:
        print(f"La función no es continua en el punto: {puntoCritico}")
    
       



continuidadDeFuncion(PUNTO_CRITICO)

ctk.set_appearance_mode("dark") # MODO OSCURO PARA LA INTERFAZ GRÁFICA CUSTOM TKINTER

def graficarFuncion():

    EJEX = np.linspace(-100, 100, 1000) # CREAMOS UN LISTA DE NÚMEROS DESDE -100 HASTA 100 CON 1000 PUNTOS PARA GRAFICAR LA FUNCIÓN

    EJEY = []

    for x in EJEX:

        try:

            funcion = function(x)

            # evita valores infinitos gigantes
            if abs(funcion) < 10000:
                EJEY.append(funcion) # AHI SE AGREGA EL VALOR DE LA FUNCIÓN A LA LISTA DE EJE Y
            else:
                EJEY.append(np.nan)

        except:
            EJEY.append(np.nan)

    
    plt.style.use("dark_background")

    # gráfico
    plt.plot(EJEX, EJEY)

    plt.title("Grafico de la función")

    plt.xlabel("Eje X")
    plt.ylabel("Eje Y")

    plt.grid()

    plt.show()



# VENTANA CUSTOMTKINTER

app = ctk.CTk()

app.geometry("400x200")

app.title("Graficador")



# EJECUTAR AUTOMÁTICAMENTE

graficarFuncion()



# LOOP

app.mainloop()

