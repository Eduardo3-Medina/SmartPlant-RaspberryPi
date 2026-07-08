import random
from datetime import datetime


def generar_datos():

    temperatura = round(random.uniform(18, 35), 1)

    humedad = random.randint(20, 80)

    hora = datetime.now().strftime("%H:%M:%S")

    return temperatura, humedad, hora