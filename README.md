# 💡 Sistema de Iluminación Pública Inteligente

**Autores:** Josué Alejandro Esparza Padilla y Gilberto Fabián Correa González  
_Proyecto final de la materia Aplicaciones de IoT_

---

## 🌟 Características Clave

- 📡 **Detección en tiempo real** de sonido, obstáculos y presencia de gases.
- 🌦️ **Monitoreo ambiental** con sensores analógicos y digitales.
- 📊 **Visualización en Node-RED Dashboard** con gráficas, tablas y alertas.
- 📧 **Sistema de alertas MQTT** con buzzer, LED RGB y control OLED.
- 🗃️ **Registro histórico** en base de datos PostgreSQL.
- 💙 **Control remoto del buzzer** desde el panel en Node-RED.

---

## 🧱 Arquitectura del Sistema

```mermaid
graph TD;
    subgraph Entrada
    mic[Sensor de Sonido] --> ESP32
    ir[Sensor de Obstáculo] --> ESP32
    gas[Sensor de Gas MQ-135] --> ESP32
    dist[Sensor Ultrasónico HC-SR04] --> ESP32
    end

    ESP32 -->|WiFi + MQTT| RaspberryPi
    ESP32 --> Actuadores

    RaspberryPi --> Dashboard[Node-RED Dashboard]
    RaspberryPi --> PostgreSQL[(Base de Datos)]

    Actuadores --> Buzzer
    Actuadores --> LED[Tira LED RGB]
    Actuadores --> OLED[Display OLED I2C]
```

---

## 🔧 Especificaciones Técnicas Detalladas

### ⚙️ Hardware

| Componente           | Especificaciones Técnicas                    | Ubicación en el Sistema            |
|----------------------|----------------------------------------------|------------------------------------|
| ESP32                | WiFi 802.11 b/g/n, Bluetooth 4.2             | Unidad central de control          |
| Micrófono Sensible   | Voltaje: 3.3V, Salida Analógica              | Cerca de una ventana               |
| Sensor de Obstáculo  | Infrarrojo digital, rango 2-30 cm            | Junto a la puerta                  |
| Sensor de Gas        | MQ-135, Salida digital                       | Techo de la caseta                 |
| Buzzer               | 5V, 2-4kHz                                   | Parte de arriba de la caset        |
| Tira LED RGB         | WS2812B, 10 LEDs                             | Iluminación principal              |
| Pantalla OLED        | SSD1306, I2C 128x64                          | Visualicación de alerta            |

---

## 🖥️ Dashboard y Node-RED

| Nodos de Node-Red | Dashboard |Dashboard |
|---|---|---|
|<img src="https://drive.google.com/uc?export=view&id=1vNUldJlPyMZnleV5JqK4-F8ve4qK_mho" width="700"/>|<img src="https://drive.google.com/uc?export=view&id=1mybJToN9T29-eRmR6oX4Cq77A23HgQN5" width="600"/><img src="https://drive.google.com/uc?export=view&id=1sAAg9sOGAbtJZCi5s9RmMx_dXv4COUhG" width="600"/>|

---

## 🛠️ Desarrollo del Prototipo

| Montaje y pruebas | Materiales usados | Cableado interno |
|------------------|-------------------|------------------|
| <img src="https://drive.google.com/uc?export=view&id=1ZY5g-Fs7_Pl2my0fGD6A7laokcmQwGKm" width="500"/> | <img src="https://drive.google.com/uc?export=view&id=1sHjKcKTSXX22XKSqmGwYFCTMGYzElB93" width="500"/>  | <img src="https://drive.google.com/uc?export=view&id=1FYR72bXAjQUmYC6KbE7qlxV5l1ecEUsT" width="500"/> |
---

## 🔎 Validación del Proyecto

🎮 **Video de validación del sistema:**  

<a href="https://drive.google.com/file/d/1HtmbRq3sqZ412pA8bL9V3XrinhruwEJE/view?usp=sharing">Validación y Retroalimentación del proyecto</a>

---

## 🏆 Resultados Obtenidos

📹 **Resultados en funcionamiento:**  
https://youtu.be/vdBM9zzcJOw

---


