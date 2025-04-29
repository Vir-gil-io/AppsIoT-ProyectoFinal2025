import network, machine
from machine import Pin, I2C
import ssd1306, neopixel
from umqtt.simple import MQTTClient
from time import sleep_ms, sleep_us, ticks_ms

# ————— CONFIGURACIÓN WiFi/MQTT —————
SSID         = 'DESKTOP-LU8P09G 2015'
PASSWORD     = '39w2F61?'
MQTT_BROKER  = 'broker.emqx.io'
TOPIC_SET    = b'caseta/luz/set'
TOPIC_STATE  = b'caseta/luz/state'
TOPIC_MSG    = b'caseta/luz/msg'
TOPIC_DIST   = b'caseta/distancia'
CLIENT_ID    = 'esp32_caseta'

# ————— OLED 128×64 I2C —————
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
def dividir_texto(txt, ancho=16):
    líneas = []
    while txt:
        líneas.append(txt[:ancho]); txt = txt[ancho:]
    return líneas
def mostrar_mensaje_multilinea(msg):
    oled.fill(0)
    for i, lin in enumerate(dividir_texto(msg)):
        if i >= 8: break
        oled.text(lin, 0, i*8)
    oled.show()

# ————— TIRA WS2812B —————
NUM_LEDS = 60
leds     = neopixel.NeoPixel(Pin(15), NUM_LEDS)
def arcoiris(p):
    for i in range(NUM_LEDS):
        leds[i] = ((i*5+p)%256, (i*2+p)%256, (i*3+p)%256)
    leds.write()
def apagar_tira():
    for i in range(NUM_LEDS):
        leds[i] = (0,0,0)
    leds.write()

# ————— HC-SR04 —————
TRIG = Pin(18, Pin.OUT)
ECHO = Pin(19, Pin.IN)
def medir_distancia_cm():
    TRIG.value(0); sleep_us(2)
    TRIG.value(1); sleep_us(10)
    TRIG.value(0)
    try:
        dur  = machine.time_pulse_us(ECHO, 1, 30000)
        dist = dur / 58.0
        return dist
    except OSError:
        return None

# ————— Conexión WiFi —————
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Conectando a WiFi", end="")
    while not wlan.isconnected():
        print(".", end="")
        sleep_ms(300)
    print("\nWiFi OK:", wlan.ifconfig())

# ————— Lógica MQTT + control —————
manual_led      = False
estado_actual   = False
last_detect     = 0
first_measure   = False
last_switch_ms  = 0
DEBOUNCE_MS     = 300

def on_mqtt(topic, msg):
    global manual_led, last_switch_ms
    txt   = msg.decode().strip()
    ahora = ticks_ms()
    if topic == TOPIC_SET:
        if ahora - last_switch_ms > DEBOUNCE_MS:
            manual_led     = (txt == '1')
            last_switch_ms = ahora
            print("Switch MQTT:", manual_led)
    elif topic == TOPIC_MSG:
        print("Mensaje OLED:", txt)
        mostrar_mensaje_multilinea(txt)

def publicar_estado(val):
    client.publish(TOPIC_STATE, b'1' if val else b'0', retain=True)

# ————— Inicio —————
conectar_wifi()

client = MQTTClient(CLIENT_ID, MQTT_BROKER)
client.set_callback(on_mqtt)
client.connect()
client.subscribe(TOPIC_SET)
client.subscribe(TOPIC_MSG)
print("Suscrito a:", TOPIC_SET.decode(), "y", TOPIC_MSG.decode())

mostrar_mensaje_multilinea("Esperando comandos")

paso   = 0
t_led  = ticks_ms()
t_dist = ticks_ms()

while True:
    client.check_msg()

    # medir distancia c/500 ms
    if ticks_ms() - t_dist > 500:
        d = medir_distancia_cm()
        if d is not None:
            dist = round(d,1)
            print("Distancia:", dist, "cm")
            client.publish(TOPIC_DIST, str(dist), retain=True)
            # Habilita primera lectura y actualiza last_detect sólo si ≤10 cm
            first_measure = True
            if 0 < d <= 10:
                last_detect = ticks_ms()
        t_dist = ticks_ms()

    # sensor sólo activo tras primera lectura
    if first_measure:
        sensor_active = (ticks_ms() - last_detect) <= 5000
    else:
        sensor_active = False

    # combinar manual + sensor
    deseado = manual_led or sensor_active

    # expira sensor_active → forzar OFF si switch no está ON
    if not sensor_active and not manual_led and estado_actual:
        deseado = False

    # al cambiar estado, actuar y publicar
    if deseado != estado_actual:
        estado_actual = deseado
        if estado_actual:
            print("TIRA: ON")
            t_led = ticks_ms()
        else:
            print("TIRA: OFF")
            apagar_tira()
        publicar_estado(estado_actual)

    # animación arcoíris si ON
    if estado_actual and ticks_ms() - t_led > 50:
        arcoiris(paso)
        paso = (paso + 1) % 256
        t_led = ticks_ms()

    sleep_ms(10)
