def analizar(temperatura, humedad):

    if humedad < 40:
        estado = "Necesita riego"
        bomba = "ENCENDIDA"
        color_estado = "red"
        color_bomba = "green"
    else:
        estado = "Normal"
        bomba = "APAGADA"
        color_estado = "green"
        color_bomba = "red"

    return estado, bomba, color_estado, color_bomba