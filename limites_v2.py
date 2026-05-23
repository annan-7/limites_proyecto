import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
from sympy import limit, Symbol, sympify




# Variable simbólica con que se trabajará

x = Symbol('x')

# Config custom tkinter

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.geometry("1000x600")
app.title("Calculadora de Límites")



# Frame superior para botones
frame_superior = ctk.CTkFrame(app)
frame_superior.pack(
    side="top",
    fill="x",
    padx=10,
    pady=10
)

# Frame izquierdo para inputs y resultados
frame_izquierdo = ctk.CTkFrame(app)
frame_izquierdo.pack(
    side="left",
    fill="y",
    padx=10,
    pady=10
)

# Frame derecho para gráfico(Matplotlib)
frame_derecho = ctk.CTkFrame(app)
frame_derecho.pack(
    side="right",
    fill="both",
    expand=True,
    padx=10,
    pady=10
)



# Titulo
titulo = ctk.CTkLabel(
    frame_izquierdo,
    text="Calculadora de Límites",
    font=("Arial", 24)
)
titulo.pack(pady=20)



# Input Funcion
entrada_funcion = ctk.CTkEntry(
    frame_izquierdo,
    width=250,
    placeholder_text="Ingrese f(x)"
)
entrada_funcion.pack(pady=10)



# Input valor de a
entrada_a = ctk.CTkEntry(
    frame_izquierdo,
    width=250,
    placeholder_text="Ingrese valor de a"
)
entrada_a.pack(pady=10)



# Label para mostrar resultados
resultado_label = ctk.CTkLabel(
    frame_izquierdo,
    text="Resultado:"
)
resultado_label.pack(pady=20)



# Figura y ejes para Matplotlib
fig, ax = plt.subplots(figsize=(6, 5))
fig.patch.set_facecolor("#2b2b2b")
ax.set_facecolor("#2b2b2b")
ax.set_title("Gráfico")
ax.set_xlabel("Eje X")
ax.set_ylabel("Eje Y")

ax.title.set_color("white")
ax.xaxis.label.set_color("white")
ax.yaxis.label.set_color("white")
ax.tick_params(colors="white")

ax.grid()




# Insertar gráfico en el frame derecho
canvas = FigureCanvasTkAgg(
    fig,
    master=frame_derecho
)
canvas.draw()


    
canvas.get_tk_widget().pack(
    fill="both",
    expand=True
)

# Toolbar de Matplotlib
toolbar = NavigationToolbar2Tk(
    canvas,
    frame_derecho
)

toolbar.update()
toolbar.pan()



# Obtener datos de los inputs
def obtener_datos():
    funcion_texto = entrada_funcion.get()
    valor_a = float(entrada_a.get())
    expresion = sympify(funcion_texto)
    return expresion, valor_a



# Función para graficar la función y el valor de a

def graficar_funcion(expresion, valor_a):
    #expersio es la función y valor_a es a que se tiende el x
   
    x_vals = []
    y_vals = []
    valor = -10
    
    #En el while loop estamos generando los valores de x e y para graficar la función, 
    # pero solo graficamos los valores de y que no sean muy grandes (menores a 100) 
    # para evitar que el gráfico se vea distorsionado por valores extremos.
    while valor <= 10:
        try:
            if abs(valor) < 0.001:
               valor += 0.01
               continue
            y = expresion.subs(x, valor).evalf()
            
            x_vals.append(valor)
            y_vals.append(y)
        except:
            pass
        valor += 0.01
    #Theme de gráfico
    ax.set_facecolor("#2b2b2b")


    
    ax.axvline(
      x=valor_a,
      linestyle="--",
      color="red"
    )
    limite = limit(
      expresion,
      x,
      valor_a
    )
    ax.plot(
       valor_a,
       float(limite),
       marker='o',
       markersize=10,
       markerfacecolor='none',
       markeredgecolor='yellow'
    )
    ax.plot(
        x_vals,
        y_vals,
        color="#ffffff"
    )
    
    ax.grid(color="gray")
    ax.title.set_color("white")
    # cambiar el color de los ejes y las etiquetas a blanco para que se vean en el tema oscuro
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.tick_params(colors="white")
    canvas.draw()



# Límite finito

def calcular_limite_finito():
    try:
        expresion, valor_a = obtener_datos()
        limite = limit(
            expresion,
            x,
            valor_a
        )
        if limite.is_finite:
            resultado_label.configure(
                text=f"Límite finito: {limite}"
            )
        else:
            resultado_label.configure(
                text="El límite no es finito"
            )
        graficar_funcion(
            expresion,
            valor_a
        )
    except Exception as e:
        resultado_label.configure(
            text=f"Error: {e}"
        )

#Calcular limite de todo los tipo 
def calcular_limite():
    try:
        expresion, valor_a = obtener_datos()
        limite = limit(
            expresion,
            x,
            valor_a
        )
        resultado_label.configure(
            text=f"Límite: {limite}"
        )
        graficar_funcion(
            expresion,
            valor_a
        )

    except Exception as e:
        resultado_label.configure(
            text=f"Error: {e}"
        )

# Límite infinito
def calcular_limite_infinito():
    try:
        expresion, valor_a = obtener_datos()
        limite = limit(
            expresion,
            x,
            valor_a
        )
        if limite.is_infinite:
            resultado_label.configure(
                text=f"Límite infinito: {limite}"
            )
        else:
            resultado_label.configure(
                text="El límite no es infinito"
            )
        graficar_funcion(
            expresion,
            valor_a
        )

    except Exception as e:
        resultado_label.configure(
            text=f"Error: {e}"
        )



# Límites laterales

def calcular_limites_laterales():
    try:
        expresion, valor_a = obtener_datos()
        izquierda = limit(
            expresion,
            x,
            valor_a,
            "-"
        )
        derecha = limit(
            expresion,
            x,
            valor_a,
            "+"
        )
        if izquierda == derecha:

            resultado_label.configure(
                text=f"Límite lateral: {izquierda}"
            )
        else:
            resultado_label.configure(
                text=f"Izq: {izquierda} | Der: {derecha}"
            )
        graficar_funcion(
            expresion,
            valor_a
        )
    except Exception as e:
        resultado_label.configure(
            text=f"Error: {e}"
        )

def limpiar_grafico():

    ax.clear()

    ax.set_title("Gráfico")
    ax.set_xlabel("Eje X")
    ax.set_ylabel("Eje Y")

    ax.set_facecolor("#2b2b2b")

    ax.grid(color="gray")

    ax.title.set_color("white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.tick_params(colors="white")

    canvas.draw()

    resultado_label.configure(
        text="Resultado:"
    )

btn_limpiar = ctk.CTkButton(
    frame_superior,
    text="Limpiar",
    command=limpiar_grafico
)

btn_limpiar.pack(
    side="left",
    padx=10
)
# Botón para calcular límite en frame izquierdo
 
boton_calcular = ctk.CTkButton(
    frame_izquierdo,
    text="Calcular Límite",
    command=calcular_limite
)

boton_calcular.pack(pady=10)


# Botones superiores para calcular límites(finito, infinito, laterales)
btn_finito = ctk.CTkButton(
    frame_superior,
    text="Límite Finito",
    command=calcular_limite_finito
)
btn_finito.pack(
    side="left",
    padx=10
)
btn_infinito = ctk.CTkButton(
    frame_superior,
    text="Límite Infinito",
    command=calcular_limite_infinito
)
btn_infinito.pack(
    side="left",
    padx=10
)
btn_laterales = ctk.CTkButton(
    frame_superior,
    text="Límites Laterales",
    command=calcular_limites_laterales
)
btn_laterales.pack(
    side="left",
    padx=10
)

# LOOP PRINCIPAL

app.mainloop()
