// Pines de los componentes (Configuración estándar)
const int pinHumedad = A0;      // Sensor de Humedad de suelo
const int pinTemperatura = A1;  // Sensor de Temperatura TMP36
const int pinBombaLED = 13;     // LED que simula la bomba de agua

unsigned long previoMillis = 0;
const long intervalo = 2000;    // Enviar datos cada 2 segundos

void setup() {
  Serial.begin(9600);           // Velocidad de comunicación serial
  pinMode(pinBombaLED, OUTPUT);
  digitalWrite(pinBombaLED, LOW); // Bomba inicialmente apagada
}

void loop() {
  unsigned long actualMillis = millis();

  // 1. ENVIAR DATOS CADA 2 SEGUNDOS A LA RASPBERRY PI
  if (actualMillis - previoMillis >= intervalo) {
    previoMillis = actualMillis;

    // Leer Sensor de Humedad (mapeado de 0 a 100%)
    int lecturaHum = analogRead(pinHumedad);
    int humedad = map(lecturaHum, 0, 1023, 0, 100); 

    // Leer Sensor de Temperatura TMP36
    int lecturaTemp = analogRead(pinTemperatura);
    float voltaje = lecturaTemp * (5.0 / 1023.0);
    float temperatura = (voltaje - 0.5) * 100.0; // Conversión a °C

    // Enviar formato "temperatura,humedad" -> Ej: "26.8,45"
    Serial.print(temperatura, 1);
    Serial.print(",");
    Serial.println(humedad);
  }

  // 2. ESCUCHAR ÓRDENES DE CONTROL DE LA RASPBERRY PI
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim(); // Limpiar espacios sueltos

    if (comando == "ON") {
      digitalWrite(pinBombaLED, HIGH); // Raspberry ordena encender riego
    } else if (comando == "OFF") {
      digitalWrite(pinBombaLED, LOW);  // Raspberry ordena apagar riego
    }
  }
}