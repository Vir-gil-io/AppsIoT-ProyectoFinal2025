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
    Sensores --> ESP32
    ESP32 --> RaspberryPi
    ESP32 --> Actuadores
    RaspberryPi --> Dashboard[Node-RED Dashboard]
    Actuadores --> Buzzer
    Actuadores --> LED[Tira LED RGB]
    Actuadores --> OLED[Display OLED I2C]
    RaspberryPi --> PostgreSQL[(Base de Datos)]
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

## 🖥️ Dashboard en Node-RED

![Dashboard](./imagenes/dashboard.png)

---

## 🛠️ Desarrollo del Prototipo

| Montaje y pruebas | Materiales usados | Cableado interno |
|------------------|-------------------|------------------|
| https://drive.google.com/file/d/1YMDx8jCyPzG6F7v1iNe2TzXgGcczu9_W/view?usp=sharing | ![foto2](./imagenes/montaje2.png) | ![foto3](./imagenes/montaje3.png) | ![foto2](./imagenes/montaje2.png) | ![foto3](./imagenes/montaje3.png) |

---

## 🔎 Validación del Proyecto

🎮 **Video de validación del sistema:**  
[![Video Validación](https://img.shields.io/badge/YouTube-Ver%20Video-red?logo=youtube)](https://youtu.be/F0IYwWB71fs?si=4-UIC3-dEtw0dK1x)

---

## 🏆 Resultados Obtenidos

📹 **Resultados en funcionamiento:**  
[![Resultados](https://img.shields.io/badge/YouTube-Resultados%20Obtenidos-blue?logo=youtube)](https://youtu.be/sRgUl2rID08?si=QA6XuITk5DwffLi7)

---


