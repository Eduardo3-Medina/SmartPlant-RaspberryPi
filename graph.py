import tkinter as tk
from tkinter import messagebox
import os
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def abrir_grafico(ventana_principal):
    ruta_csv = os.path.join("data", "historial.csv")
    # Verificación si existen datos iniciales
    if not os.path.exists(ruta_csv):
        messagebox.showwarning("Sin datos", "No hay un historial guardado en CSV para graficar todavía. Inicia el monitoreo primero.")
        return
    # Crear Ventana Secundaria en Tkinter
    ventana_grafico = tk.Toplevel(ventana_principal)
    ventana_grafico.title("📊 Gráficos en Tiempo Real - SmartPlant")
    ventana_grafico.geometry("700x570")
    ventana_grafico.configure(bg="#F5F5F5")
    # Crear la figura de Matplotlib (2 subgráficos en una columna)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 5), sharex=True)
    fig.patch.set_facecolor('#F5F5F5')
    # Integrar el gráfico de Matplotlib dentro de la ventana de Tkinter
    canvas = FigureCanvasTkAgg(fig, master=ventana_grafico)
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    # --- FUNCIÓN INTERNA DE ACTUALIZACIÓN ---
    def actualizar_lineas_grafico():
        if not ventana_grafico.winfo_exists():
            return
        horas = []
        temperaturas = []
        humedades = []
        # 1. Re-leer el archivo CSV 
        try:
            with open(ruta_csv, "r", encoding="utf-8") as archivo:
                lector = csv.reader(archivo)
                next(lector)  
                for fila in lector:
                    if len(fila) >= 3:
                        horas.append(fila[0])
                        temperaturas.append(float(fila[1]))
                        humedades.append(float(fila[2]))
        except Exception:
            ventana_grafico.after(2000, actualizar_lineas_grafico)
            return

        # 2. Si hay datos, limpiar y redibujar
        if horas:
            max_puntos = 12
            horas_recientes = horas[-max_puntos:]
            temps_recientes = temperaturas[-max_puntos:]
            hums_recientes = humedades[-max_puntos:]

            # Limpiar ejes anteriores
            ax1.clear()
            ax2.clear()

            # Redibujar Subgráfico 1: Temperatura
            ax1.plot(horas_recientes, temps_recientes, color="#FF5722", marker="o", linestyle="-", linewidth=2)
            ax1.set_ylabel("Temperatura (°C)", color="#FF5722", fontweight="bold")
            ax1.tick_params(axis='y', labelcolor="#FF5722")
            ax1.grid(True, linestyle="--", alpha=0.6)
            ax1.set_title("Monitoreo Dinámico de Sensores (En Vivo)", fontsize=11, fontweight="bold", pad=5)

            # Redibujar Subgráfico 2: Humedad
            ax2.plot(horas_recientes, hums_recientes, color="#2196F3", marker="s", linestyle="-", linewidth=2)
            ax2.set_ylabel("Humedad (%)", color="#2196F3", fontweight="bold")
            ax2.set_xlabel("Hora de Lectura", fontweight="bold")
            ax2.tick_params(axis='y', labelcolor="#2196F3")
            ax2.grid(True, linestyle="--", alpha=0.6)

            # Ajustar diseño de etiquetas de tiempo rotadas
            for label in ax2.get_xticklabels():
                label.set_rotation(45)
                label.set_horizontalalignment('right')

            fig.tight_layout()
            canvas.draw()  # Refrescar el lienzo en la pantalla

        # 3. Volver a llamar a esta función dentro de 2000 ms (2 segundos)
        ventana_grafico.after(2000, actualizar_lineas_grafico)

    # Lanzar la primera actualización automática
    actualizar_lineas_grafico()

    # Botón inferior para cerrar
    tk.Button(
        ventana_grafico, 
        text="Cerrar Gráfico", 
        command=ventana_grafico.destroy, 
        bg="#9E9E9E", 
        fg="white", 
        font=("Arial", 10, "bold"),
        pady=5
    ).pack(pady=10)