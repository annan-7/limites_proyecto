import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import Symbol, sympify, oo, simplify, zoo, nan 


# 1. CONFIGURACIÓN INICIAL

x = Symbol('x')

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1000x650")
app.title("Analizador de Límites")


# 2. LÓGICA MATEMÁTICA PASO A PASO 



def evaluar_limite_con_logica(expr, h_val):
    """
    Algoritmo propio que evalúa el límite paso a paso usando 
    ciclos, condicionales y manipulación algebraica con SymPy.
    """
    historial_pasos = []

    # PASO 1: Intentar sustitución directa (solo si h es finito)
    if h_val not in [oo, -oo]:
        try:
            res_directo = expr.subs(x, h_val).evalf()
            if res_directo.is_finite and not res_directo.has(nan, zoo):
                historial_pasos.append("1. Sustitución directa exitosa.")
                return float(res_directo), historial_pasos
        except Exception:
            pass
    else:
        historial_pasos.append("1. Límite al infinito. Sustitución directa no aplica.")

    # PASO 2: Manipulación algebraica (solo si h es finito)
    if h_val not in [oo, -oo]:
        try:
            expr_simplificada = simplify(expr)
            historial_pasos.append(f"2. Indeterminación detectada. Se simplificó a: {expr_simplificada}")
            
            res_simplificado = expr_simplificada.subs(x, h_val).evalf()
            if res_simplificado.is_finite and not res_simplificado.has(nan, zoo):
                historial_pasos.append("3. Sustitución directa tras simplificar fue exitosa.")
                return float(res_simplificado), historial_pasos
        except Exception:
            pass
    else:
        historial_pasos.append("2. Intentando análisis de comportamiento asintótico...")

    # PASO 3: Aproximación numérica mediante ciclos (Límites laterales O al infinito)
    if h_val not in [oo, -oo]:
        h_float = float(h_val)
        aprox_izq, aprox_der = None, None
        
        historial_pasos.append("3. Aplicando aproximación numérica (Límites laterales con ciclo for):")
        
        for epsilon in [0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001]:
            val_izq = h_float - epsilon
            val_der = h_float + epsilon
            
            try:
                y_izq = float(expr.subs(x, val_izq).evalf())
                y_der = float(expr.subs(x, val_der).evalf())
                
                if abs(y_izq) < 1000: aprox_izq = y_izq
                if abs(y_der) < 1000: aprox_der = y_der
                
            except Exception:
                pass
            
           

        if aprox_izq is not None and aprox_der is not None:
            promedio = (aprox_izq + aprox_der) / 2
            tolerancia = max(0.01, 0.001 * (abs(aprox_izq) + abs(aprox_der)) / 2)
            if abs(aprox_izq - aprox_der) < tolerancia:
                historial_pasos.append(f"   - Los límites laterales convergen a: {promedio:.6f}")
                return round(promedio, 6), historial_pasos
            else:
                historial_pasos.append(f"   - Límites laterales divergen: Izq ≈ {aprox_izq:.4f}, Der ≈ {aprox_der:.4f}")
                return "No existe", historial_pasos
        else:
            historial_pasos.append("   - La función tiende a infinito cerca de h.")
            return "Infinito", historial_pasos
            
    else:
        # NUEVA LÓGICA PARA LÍMITES AL INFINITO O -INFINITO
        historial_pasos.append("3. Evaluando comportamiento en valores muy grandes (ciclo for):")
        
        # Generamos valores gigantes: 10, 100, 1000, 10000, 100000
        valores_grandes = [10**i for i in range(1, 6)]
        resultados = []
        
        for val in valores_grandes:
            try:
                # Si es -oo, evaluamos en valores negativos gigantes
                eval_val = -val if h_val == -oo else val
                y = float(expr.subs(x, eval_val).evalf())
                resultados.append(y)
                historial_pasos.append(f"   - f({eval_val}) = {y:.6f}")
            except Exception:
                resultados.append(None)
        
        # Analizamos si los resultados convergen a un número finito
        resultados_validos = [r for r in resultados if r is not None and abs(r) < 10000]
        
        if len(resultados_validos) >= 3:
            # Verificamos si los últimos 3 valores son casi iguales (convergen)
            ultimos_tres = resultados_validos[-3:]
            if max(ultimos_tres) - min(ultimos_tres) < 0.1:
                promedio = sum(ultimos_tres) / len(ultimos_tres)
                historial_pasos.append(f"4. Los valores convergen a: {promedio:.4f}")
                return round(promedio, 4), historial_pasos
        
        # Si no convergen, verificamos si crecen infinitamente
        if all(r is not None and abs(r) > 1000 for r in resultados[-2:]):
            historial_pasos.append("4. Los valores crecen sin límite → El límite es Infinito.")
            return "Infinito", historial_pasos
        
        historial_pasos.append("4. Comportamiento no determinado numéricamente.")
        return "Indeterminado", historial_pasos


def obtener_datos():
    func_str = entrada_funcion.get().strip()
    h_str = entrada_h.get().strip().lower()

    if not func_str or not h_str:
        raise ValueError("Ingrese función y valor de h.")

    if h_str in ['oo', 'inf', ' infinito']:
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
    ax.clear()
    y_vals = []
    h_float = None

    if h_val in [oo, -oo]:
        rango_x = [i * 0.1 for i in range(-100, 101)]
    else:
        h_float = float(h_val)
        rango_x = [h_float - 5.0 + i * 0.05 for i in range(200)]

    for val in rango_x:
        try:
            if h_val not in [oo, -oo] and abs(val - h_float) < 0.001:
                y_vals.append(None)
                continue

            y = float(expr.subs(x, val).evalf())
            if abs(y) < 100:
                y_vals.append(y)
            else:
                y_vals.append(None)
        except Exception:
            y_vals.append(None)

    ax.set_facecolor("#2b2b2b")
    ax.grid(color="gray", linestyle="--", alpha=0.7)
    ax.set_title("Comportamiento de la función", color="white", fontsize=12)
    ax.set_xlabel("x", color="white")
    ax.set_ylabel("f(x)", color="white")
    ax.tick_params(colors="white")

    ax.plot(rango_x, y_vals, color="#00ff00", label="f(x)", linewidth=2)

    if h_val not in [oo, -oo]:
        ax.axvline(x=float(h_val), linestyle="--", color="red", label=f"x = {h_val}")
        
    ax.legend(facecolor="#2b2b2b", edgecolor="white", labelcolor="white")
    canvas.draw()


def calcular_y_graficar():
    try:
        expr, h_val = obtener_datos()
        
        # AQUÍ LLAMAMOS A NUESTRO ALGORITMO PASO A PASO
        resultado, pasos_logicos = evaluar_limite_con_logica(expr, h_val)
        
        # Mostrar resultado
        resultado_label.configure(
            text=f"Resultado:\n{resultado}",
            text_color="#00ff00" if isinstance(resultado, (int, float)) else "orange"
        )
        
        # Mostrar la lógica en un área de texto para que el profesor la VEAN
        texto_pasos = "Desarrollo Lógico del Algoritmo:\n" + "\n".join(pasos_logicos)
        pasos_label.configure(text=texto_pasos)

        graficar_funcion(expr, h_val)

    except Exception as e:
        resultado_label.configure(text=f"Error:\n{str(e)[:120]}", text_color="red")
        pasos_label.configure(text="Sin resultado — revisa la sintaxis.")
        ax.clear()
        ax.set_facecolor("#2b2b2b")
        canvas.draw()


# 3. INTERFAZ DE USUARIO (UI/UX)

frame_izquierdo = ctk.CTkFrame(app, width=350)
frame_izquierdo.pack(side="left", fill="y", padx=10, pady=10)

frame_derecho = ctk.CTkFrame(app)
frame_derecho.pack(side="right", fill="both", expand=True, padx=10, pady=10)

ctk.CTkLabel(frame_izquierdo, text="Calculadora de Límites\n(Lógica Algorítmica)", font=("Arial", 18, "bold")).pack(pady=(10, 20))

ctk.CTkLabel(frame_izquierdo, text="Función f(x):", anchor="w").pack(fill="x", padx=10)
entrada_funcion = ctk.CTkEntry(frame_izquierdo, placeholder_text="Ej: (x**2 - 1)/(x - 1)")
entrada_funcion.pack(fill="x", padx=10, pady=(0, 10))

ctk.CTkLabel(frame_izquierdo, text="Valor h (tiende a):", anchor="w").pack(fill="x", padx=10)
entrada_h = ctk.CTkEntry(frame_izquierdo, placeholder_text="Ej: 1, 0, oo")
entrada_h.pack(fill="x", padx=10, pady=(0, 20))

btn_calcular = ctk.CTkButton(frame_izquierdo, text="Ejecutar Algoritmo y Graficar", command=calcular_y_graficar, height=40, fg_color="#1f6aa5")
btn_calcular.pack(fill="x", padx=10, pady=10)

resultado_label = ctk.CTkLabel(frame_izquierdo, text="Resultado:\nEsperando...", font=("Arial", 16, "bold"), wraplength=320, justify="left")
resultado_label.pack(fill="x", padx=10, pady=10)

# NUEVO: Label para mostrar los pasos lógicos 
pasos_label = ctk.CTkLabel(frame_izquierdo, text="", font=("Consolas", 11), wraplength=320, justify="left", fg_color="#1e1e1e", corner_radius=5)
pasos_label.pack(fill="both", expand=True, padx=10, pady=10)

fig, ax = plt.subplots(figsize=(6, 5))
fig.patch.set_facecolor("#2b2b2b")
ax.set_facecolor("#2b2b2b")
canvas = FigureCanvasTkAgg(fig, master=frame_derecho)
canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    app.mainloop()
