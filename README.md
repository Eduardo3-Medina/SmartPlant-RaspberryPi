# 🌱 SmartPlant - Plataforma Inteligente de Monitoreo y Automatización

## 1. Descripción del Proyecto y Problemática Real
En entornos urbanos y agricultura doméstica, la falta de tiempo y el desconocimiento técnico suelen provocar la pérdida de cultivos debido a riegos inadecuados o exposición a temperaturas extremas. 

**SmartPlant** es una solución tecnológica e inteligente basada en la arquitectura **Edge Computing**, que integra una **Raspberry Pi** y un **Arduino Uno** para monitorear en tiempo real las variables ambientales de una planta (temperatura y humedad del suelo), automatizando el proceso de riego de manera óptima para preservar la salud del cultivo sin intervención humana constante.

---

## 2. Cumplimiento de Requisitos del Enunciado

### 🛠️ Hardware (Arquitectura Diseñada)
El sistema está completamente diseñado y estructurado para soportar los siguientes componentes físicos:
* **Cerebro Central:** 1 Raspberry Pi (Procesamiento, almacenamiento y UI).
* **Módulo de Adquisición:** 1 Arduino Uno (Lectura de sensores en tiempo real).
* **Sensores (Dispositivos de entrada):**
    * Sensor de Humedad de Suelo (Conectado al pin analógico `A0`).
    * Sensor de Temperatura TMP36 (Conectado al pin analógico `A1`).
* **Actuador (Dispositivo de salida):**
    * Bomba de Agua / LED Indicador de Riego (Conectado al pin digital `13`).

### 💻 Software y Capas del Sistema
El repositorio está organizado de forma modular siguiendo estándares profesionales:
* **`/arduino/SmartPlant.ino`:** Programa nativo en C++ para el Arduino Uno encargado de la lectura síncrona de los sensores y la escucha de comandos directos por bus serial.
* **Aplicación Raspberry Pi (Python):** Código robusto multihilo estructurado en:
    * `app.py`: Punto de entrada principal del sistema.
    * `interfaz.py`: Panel visual responsivo desarrollado en **Tkinter**.
    * `graph.py`: Gráficos dinámicos animados en tiempo real utilizando **Matplotlib**.
    * `logic.py`: Procesamiento de información y lógica de automatización.
    * `simulator.py`: Emulador de hardware para pruebas de entorno.

### 🔌 Comunicación (USB Serial / Arquitectura Híbrida)
La comunicación entre dispositivos se realiza mediante **USB Serial a 9600 baudios**, utilizando strings formateados (`temperatura,humedad`) para el envío de datos y comandos de texto simples (`ON` / `OFF`) para el control de actuadores.

> ⚠️ **Nota de Implementation para Evaluación:** Con el fin de garantizar la portabilidad y la evaluación del software en laboratorios sin disponibilidad inmediata del hardware físico, la aplicación en Python incluye un **Módulo de Emulación Serial**. Si el script no detecta el Arduino físico por USB, activa automáticamente este emulador que inyecta las tramas de datos respetando los tiempos del bus serial, permitiendo validar la interfaz, las gráficas y la lógica de automatización de forma idéntica a la operación real.

---

## 3. Funcionalidades Principales

1.  **Captura de Datos:** Lectura constante de temperatura (°C) y humedad de suelo (%).
2.  **Procesamiento de Información:** Filtrado de datos recibidos por el puerto serial.
3.  **Generación de Acciones Automáticas:** Si la humedad del suelo cae por debajo del umbral mínimo permitido, la Raspberry Pi procesa la alerta y envía una orden serial inmediata al Arduino para encender la bomba de agua.
4.  **Almacenamiento Local:** Los datos históricos se registran automáticamente en un archivo `.csv` dentro de la carpeta `data/` para su posterior análisis estadístico.
5.  **Interfaz de Monitoreo:** Panel gráfico de control con actualización en tiempo real.

---

## 4. Cómo Ejecutar el Proyecto

1. Clona este repositorio en tu Raspberry Pi o PC:
   ```bash
   git clone [https://github.com/Eduardo3-Medina/SmartPlant-RaspberryPi.git](https://github.com/Eduardo3-Medina/SmartPlant-RaspberryPi.git)

   Instala las dependencias necesarias:

Bash
pip install matplotlib
Ejecuta la aplicación principal:

Bash
python app.py