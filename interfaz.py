import tkinter as tk
from tkinter import ttk
from simulator import generar_datos
from logic import analizar
import csv
import os
import time  # Para el reloj en tiempo real
from graph import abrir_grafico 


class SmartPlantApp:

    def __init__(self):

        self.ventana = tk.Tk()

        self.ventana.title("🌱 SmartPlant")
        self.ventana.geometry("950x650")
        self.ventana.configure(bg="#E8F5E9")

        self.crear_interfaz()
        self.monitoreando = False

    def crear_interfaz(self):

        titulo = tk.Label(
            self.ventana,
            text="🌱 SMARTPLANT - Plataforma Inteligente",
            bg="#2E7D32",
            fg="white",
            font=("Arial", 20, "bold"),
            pady=10
        )
        titulo.pack(fill="x")

        panel = tk.Frame(self.ventana, bg="#E8F5E9")
        panel.pack(pady=20)

        # Temperatura

        tk.Label(
            panel,
            text="Temperatura",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, padx=20)

        self.lbl_temp = tk.Label(
            panel,
            text="0 °C",
            font=("Arial", 18)
        )

        self.lbl_temp.grid(row=1, column=0)

        # Humedad

        tk.Label(
            panel,
            text="Humedad",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=1, padx=20)

        self.lbl_hum = tk.Label(
            panel,
            text="0 %",
            font=("Arial", 18)
        )

        self.lbl_hum.grid(row=1, column=1)

        # Estado

        tk.Label(
            panel,
            text="Estado",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=2, padx=20)

        self.lbl_estado = tk.Label(
            panel,
            text="Esperando datos",
            font=("Arial", 14)
        )

        self.lbl_estado.grid(row=1, column=2)

        # Bomba

        tk.Label(
            panel,
            text="Bomba",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=3, padx=20)

        self.lbl_bomba = tk.Label(
            panel,
            text="APAGADA",
            font=("Arial", 14)
        )

        self.lbl_bomba.grid(row=1, column=3)

        # Barras

        barra = tk.Frame(self.ventana, bg="#E8F5E9")
        barra.pack(fill="x", padx=30)

        tk.Label(barra, text="Temperatura").pack()

        self.tempbar = ttk.Progressbar(
            barra,
            length=400,
            maximum=40
        )

        self.tempbar.pack()

        tk.Label(
            barra,
            text="Humedad"
        ).pack(pady=(10, 0))

        self.humbar = ttk.Progressbar(
            barra,
            length=400,
            maximum=100
        )

        self.humbar.pack()

        # Tabla

        self.tabla = ttk.Treeview(
            self.ventana,
            columns=("hora", "temp", "hum"),
            show="headings",
            height=10
        )

        self.tabla.heading("hora", text="Hora")
        self.tabla.heading("temp", text="Temperatura")
        self.tabla.heading("hum", text="Humedad")

        self.tabla.column("hora", width=180)
        self.tabla.column("temp", width=180)
        self.tabla.column("hum", width=180)

        self.tabla.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # Botón
        botones = tk.Frame(self.ventana, bg="#E8F5E9")
        botones.pack(pady=10)
        tk.Button(
            botones,
            text="▶ Iniciar",
            width=15,
            bg="#4CAF50",
            fg="white",
            command=self.iniciar
        ).grid(row=0, column=0, padx=10)
        tk.Button(
            botones,
            text="⏹ Detener",
            width=15,
            bg="#F44336",
            fg="white",
            command=self.detener
        ).grid(row=0, column=1, padx=10)

        tk.Button(
            botones,
            text="Simular 1 lectura",
            width=18,
            command=self.simular
        ).grid(row=0, column=2, padx=10)
        tk.Button(
            botones,
            text="📊 Ver Gráficos",
            width=15,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            command=lambda: abrir_grafico(self.ventana)
        ).grid(row=0, column=3, padx=10)

    def simular(self):

        temperatura, humedad, hora = generar_datos()

        estado, bomba, color_estado, color_bomba = analizar(
            temperatura,
            humedad
        )

        self.lbl_temp.config(text=f"{temperatura} °C")
        self.lbl_hum.config(text=f"{humedad} %")

        self.lbl_estado.config(
            text=estado,
            fg=color_estado
        )

        self.lbl_bomba.config(
            text=bomba,
            fg=color_bomba
        )

        self.tempbar["value"] = temperatura
        self.humbar["value"] = humedad

        self.tabla.insert(
            "",
            "end",
            values=(
                hora,
                temperatura,
                humedad
            )
        )

        # ========= GUARDAR CSV =========

        os.makedirs("data", exist_ok=True)

        ruta = os.path.join(
            "data",
            "historial.csv"
        )

        if not os.path.exists(ruta):

            with open(
                ruta,
                "w",
                newline="",
                encoding="utf-8"
            ) as archivo:

                escritor = csv.writer(archivo)

                escritor.writerow([
                    "Hora",
                    "Temperatura",
                    "Humedad",
                    "Estado",
                    "Bomba"
                ])

        with open(
            ruta,
            "a",
            newline="",
            encoding="utf-8"
        ) as archivo:

            escritor = csv.writer(archivo)

            escritor.writerow([
                hora,
                temperatura,
                humedad,
                estado,
                bomba
            ])
    def iniciar(self):

        self.monitoreando = True

        self.actualizar()


    def detener(self):

        self.monitoreando = False


    def actualizar(self):

        if self.monitoreando:

            self.simular()

            self.ventana.after(
                2000,
                self.actualizar
            )
    def run(self):

        self.ventana.mainloop()