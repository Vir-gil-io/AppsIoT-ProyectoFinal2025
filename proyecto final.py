from machine import Pin, ADC, PWM
from time import ticks_ms, ticks_diff, sleep
import network
from umqtt.simple import MQTTClient
import ujson

# -------------------- WiFi Config --------------------
ssid = "DESKTOP-LU8P09G 2015"
password = "39w2F61?"
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid, password)
while not sta_if.isconnected():
    print("Conectando al WiFi...")
    sleep(1)
print("✅ Conectado a WiFi:", sta_if.ifconfig())

# -------------------- MQTT Config --------------------
mqtt_server = "192.168.137.228"
client_id = "ESP32_SENSORES"
topic_sonido = b"sensor/sonido"
topic_obstaculo = b"sensor/obstaculo"
topic_gas = b"sensor/humo"
topic_mute = b"sensor/mute"  # ✅ Nuevo topic para silenciar

client = MQTTClient(client_id, mqtt_server)

# --- Callback para recibir mensajes ---
def callback_mqtt(topic, msg):
    global silenciado
    if topic == topic_mute:
        print("🔕 Botón presionado desde Node-RED, buzzer silenciado temporalmente.")
        silenciado = True
        buzzer.deinit()

client.set_callback(callback_mqtt)
client.connect()
print("✅ Conectado a MQTT")

# --- Suscribirse al nuevo topic ---
client.subscribe(topic_mute)

# -------------------- LED Configuration --------------------
led_microfono = Pin(5, Pin.OUT)
led_obstaculo = Pin(18, Pin.OUT)
led_gas = Pin(26, Pin.OUT)

# -------------------- Sensor Configuration --------------------
microfono = ADC(Pin(34))
microfono.atten(ADC.ATTN_11DB)
microfono.width(ADC.WIDTH_10BIT)
sensor_obstaculo = Pin(27, Pin.IN)
sensor_gas = Pin(14, Pin.IN)

# -------------------- Botón para silenciar buzzer --------------------
boton_silencio = Pin(4, Pin.IN, Pin.PULL_UP)

# -------------------- Buzzer pasivo (PWM) --------------------
buzzer = PWM(Pin(21))
buzzer.duty(512)
buzzer.deinit()

# -------------------- Umbrales --------------------
umbral_sonido = 150

# -------------------- Variables de control --------------------
led1_encendido = False
tiempo_inicio_led1 = 0

led2_encendido = False
tiempo_inicio_led2 = 0

melodia = [(262, 200), (294, 200), (330, 200), (349, 200), (392, 400)]
nota_actual = 0
tiempo_nota_inicio = 0
reproduciendo = False
silenciado = False
estado_gas_anterior = None

# -------------------- Función para revisar mensajes MQTT --------------------
def checar_mensajes_mqtt():
    try:
        client.check_msg()
    except:
        pass

# -------------------- Bucle principal --------------------
while True:
    checar_mensajes_mqtt()

    tiempo_actual = ticks_ms()

    # --- Micrófono ---
    valor_sonido = microfono.read()
    if valor_sonido > umbral_sonido:
        client.publish(topic_sonido, ujson.dumps({"sonido": valor_sonido}))
        if not led1_encendido:
            print("🔊 ¡Ruido fuerte detectado!")
            led_microfono.on()
            led1_encendido = True
            tiempo_inicio_led1 = tiempo_actual
    if led1_encendido and ticks_diff(tiempo_actual, tiempo_inicio_led1) > 5000:
        led_microfono.off()
        led1_encendido = False

    # --- Obstáculo ---
    obstaculo_detectado = sensor_obstaculo.value() == 0
    if obstaculo_detectado:
        client.publish(topic_obstaculo, ujson.dumps({"obstaculo": True}))
        if not led2_encendido:
            print("🚧 ¡Obstáculo detectado!")
            led_obstaculo.on()
            led2_encendido = True
            tiempo_inicio_led2 = tiempo_actual
    if led2_encendido and ticks_diff(tiempo_actual, tiempo_inicio_led2) > 5000:
        led_obstaculo.off()
        led2_encendido = False

    # --- Botón de silencio físico ---
    if boton_silencio.value() == 0:
        print("🔕 Botón presionado, buzzer silenciado temporalmente.")
        silenciado = True
        buzzer.deinit()

    # --- Gas detectado con estado ---
    gas_detectado = sensor_gas.value() == 0
    if gas_detectado != estado_gas_anterior:
        if gas_detectado:
            print("⚠ Humo o gas detectado ⚠")
            client.publish(topic_gas, ujson.dumps({"gas": True}))
            led_gas.on()
            if not reproduciendo:
                reproduciendo = True
                silenciado = False
                buzzer.init()
                nota_actual = 0
                tiempo_nota_inicio = tiempo_actual
        else:
            print("✅ Humo despejado.")
            client.publish(topic_gas, ujson.dumps({"gas": False}))
            led_gas.off()
            if reproduciendo:
                buzzer.deinit()
                reproduciendo = False
        estado_gas_anterior = gas_detectado

    # --- Melodía mientras el gas está activo ---
    if gas_detectado and not silenciado and reproduciendo:
        if ticks_diff(tiempo_actual, tiempo_nota_inicio) > melodia[nota_actual][1]:
            nota_actual = (nota_actual + 1) % len(melodia)
            buzzer.freq(melodia[nota_actual][0])
            tiempo_nota_inicio = tiempo_actual

    sleep(0.5)
