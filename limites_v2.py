import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import Symbol, sympify, limit, oo


# 1. CONFIGURACIÓN INICIAL Y VARIABLES GLOBALES

x = Symbol('x')

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1000x650")
app.title("Analizador y Visualizador de Límites - MATE1133")

# 2. DEFINICIÓN DE FUNCIONES (Deben ir ANTES de la UI)


def obtener_datos():
    """Obtiene y valida los datos de los campos de texto."""
    func_str = entrada_funcion.get().strip()
    h_str = entrada_h.get().strip().lower()

    if not func_str or not h_str:
        raise ValueError("Por favor, ingrese tanto la función como el valor de h.")

    # Manejo robusto de infinitos para SymPy
    if h_str in ['oo', 'inf', 'infinito']:
        h_val = oo
    elif h_str in ['-oo', '-inf', '-infinito']:
        h_val = -oo
    else:
        try:
            h_val = float(h_str)
        except ValueError:
            h_val = sympify(h_str)

    expr = sympify(func_str)
    return expr, h_val


def graficar_funcion(expr, h_val):
    """Genera la gráfica del comportamiento de la función cerca de h."""
    ax.clear() # Limpiar gráfico anterior

    x_vals = []
    y_vals = []

    # 1. Definir rango dinámico de X centrado en h
    if h_val in [oo, -oo]:
        rango_x = [i * 0.1 for i in range(-100, 101)] # Rango fijo -10 a 10
    else:
        h_float = float(h_val)
        # 200 puntos en un rango de 10 unidades centrado en h
        rango_x = [h_float - 5.0 + i * 0.05 for i in range(200)]

    # 2. Evaluar puntos usando listas puras de Python (SIN NumPy)
    for val in rango_x:
        try:
            # EVITAR evaluar exactamente en h para prevenir picos de asíntotas verticales
            if h_val not in [oo, -oo] and abs(val - h_float) < 0.001:
                y_vals.append(None) # Matplotlib ignora None, creando un salto limpio
                continue

            y = float(expr.subs(x, val).evalf())

            # Filtrar valores extremos que distorsionan la escala del gráfico
            if abs(y) < 100:
                y_vals.append(y)
            else:
                y_vals.append(None)
        except Exception:
            y_vals.append(None) # En caso de dominio inválido

    # 3. Estilizar gráfico (Tema oscuro)
    ax.set_facecolor("#2b2b2b")
    ax.grid(color="gray", linestyle="--", alpha=0.7)
    ax.set_title("Comportamiento de la función", color="white", fontsize=12)
    ax.set_xlabel("x", color="white")
    ax.set_ylabel("f(x)", color="white")
    ax.tick_params(colors="white")

    # 4. Graficar la función
    ax.plot(rango_x, y_vals, color="#00ff00", label="f(x)", linewidth=2)

    # 5. Graficar línea vertical y punto del límite (solo si h es finito)
    if h_val not in [oo, -oo]:
        ax.axvline(x=h_float, linestyle="--", color="red", label=f"x = {h_val}")
        
        try:
            lim_val = limit(expr, x, h_val)
            if lim_val.is_finite:
                ax.plot(h_float, float(lim_val), marker='o', markersize=8,
                        markerfacecolor='yellow', markeredgecolor='black', 
                        label=f"Límite = {lim_val}")
        except Exception:
            pass 

    ax.legend(facecolor="#2b2b2b", edgecolor="white", labelcolor="white")
    canvas.draw()


def calcular_y_graficar():
    """Función principal vinculada al botón de acción."""
    try:
        expr, h_val = obtener_datos()

        # Calcular el límite usando el motor simbólico de SymPy
        limite = limit(expr, x, h_val)

        # Mostrar resultado de forma inteligente en la UI
        if limite in [oo, -oo]:
            resultado_label.configure(
                text=f"El límite es:\n{limite} (Infinito)",
                text_color="orange"
            )
        elif limite.is_finite:
            resultado_label.configure(
                text=f"El límite es:\n{limite}",
                text_color="#00ff00"
            )
        else:
            resultado_label.configure(
                text=f"El límite no existe o es indeterminado:\n{limite}",
                text_color="red"
            )

        # Generar el gráfico
        graficar_funcion(expr, h_val)

    except Exception as e:
        # Manejo de errores robusto
        resultado_label.configure(
            text=f"Error:\nRevisa la sintaxis de f(x) o el valor de h.\nDetalle: {str(e)[:50]}...",
            text_color="red"
        )
        # Limpiar gráfico en caso de error
        ax.clear()
        ax.set_facecolor("#2b2b2b")
        ax.set_title("Esperando datos válidos", color="white")
        canvas.draw()



# 3. DISEÑO DE LA INTERFAZ (UI/UX)

# Frame izquierdo: Controles y resultados

frame_izquierdo = ctk.CTkFrame(app, width=300)
frame_izquierdo.pack(side="left", fill="y", padx=10, pady=10)

# Frame derecho: Gráfico (Matplotlib)
frame_derecho = ctk.CTkFrame(app)
frame_derecho.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# --- Elementos del Frame Izquierdo ---
ctk.CTkLabel(frame_izquierdo, text="Calculadora de Límites", font=("Arial", 20, "bold")).pack(pady=(10, 20))

ctk.CTkLabel(frame_izquierdo, text="Función f(x):", anchor="w").pack(fill="x", padx=10)
entrada_funcion = ctk.CTkEntry(frame_izquierdo, placeholder_text="Ej: (x**2 - 1)/(x - 1)")
entrada_funcion.pack(fill="x", padx=10, pady=(0, 10))

ctk.CTkLabel(frame_izquierdo, text="Valor h (tiende a):", anchor="w").pack(fill="x", padx=10)
entrada_h = ctk.CTkEntry(frame_izquierdo, placeholder_text="Ej: 1, 0, oo, -oo")
entrada_h.pack(fill="x", padx=10, pady=(0, 20))

# BOTÓN ÚNICO DE ACCIÓN (Ahora la función ya está definida arriba)
btn_calcular = ctk.CTkButton(
    frame_izquierdo, 
    text="Calcular Límite y Graficar", 
    command=calcular_y_graficar, 
    height=40,
    fg_color="#1f6aa5",
    hover_color="#144870"
)
btn_calcular.pack(fill="x", padx=10, pady=10)

resultado_label = ctk.CTkLabel(
    frame_izquierdo, 
    text="Resultado:\nEsperando cálculo...", 
    font=("Arial", 14), 
    wraplength=280, 
    justify="left"
)
resultado_label.pack(fill="x", padx=10, pady=20)


# 4. CONFIGURACIÓN DE MATPLOTLIB (Sin NumPy)

fig, ax = plt.subplots(figsize=(6, 5))
fig.patch.set_facecolor("#2b2b2b")
ax.set_facecolor("#2b2b2b")

# Integrar el canvas de Matplotlib en CustomTkinter
canvas = FigureCanvasTkAgg(fig, master=frame_derecho)
canvas.get_tk_widget().pack(fill="both", expand=True)


# 5. EJECUCIÓN DE LA APLICACIÓN
if __name__ == "__main__":
    app.mainloop()
