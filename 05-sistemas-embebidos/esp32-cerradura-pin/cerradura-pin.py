from machine import ADC, Timer, Pin
from neopixel import NeoPixel

# Configuración del teclado
umbral = [0, 600, 1000, 2100, 3000, 4000]
KEYS = ['RIGHT', 'UP', 'DOWN', 'LEFT', 'SELECT', None]

#Estados para el encoder
estados = {('cambio', 1): 'GIROD', ('cambio', 0): 'GIROI'}

#Variables globales
cola = []
clk_ult = 0
movimiento = None
armado = 0
cuenta = 0

# PIN correcto y PIN ingresado
pin_correcto = []
pin_ingresado = []

# Posición actual para edición de PIN
posicion_digito = 0

#Configuración de hardware
# Teclado
pin_teclado = 34
teclado = ADC(pin_teclado, atten=ADC.ATTN_11DB)

# Encoder
CLK = Pin(14, Pin.IN, Pin.PULL_UP)
DT  = Pin(27, Pin.IN, Pin.PULL_UP)
SW  = Pin(13, Pin.IN, Pin.PULL_UP)

# NeoPixels
pin_neopixel = 33
neopixel = NeoPixel(Pin(pin_neopixel), 8)

#Funciones de interrupción
def rsi(timer):
    """Lee el teclado y mete la tecla en la cola"""
    valor_actual = teclado.read()
    for i in range(5, -1, -1):
        if valor_actual >= umbral[i]:
            if i != 5:
                cola.append(KEYS[i])
            break

def rsi_encod(timer):
    """Detecta giro del encoder"""
    global clk_ult, movimiento
    clk_act = CLK.value()
    if clk_ult == 1 and clk_act == 0:
        estado_temp = 'cambio'
        movimiento = estados[(estado_temp, DT.value())]
        cola.append(movimiento)
    clk_ult = clk_act

def timer_sw(timer):
    """Confirma clic del encoder"""
    global cuenta, armado
    cuenta += 1
    cola.append('SWITCH')
    armado = 0

def sw_rsi(pin):
    """Antirrebote del encoder"""
    global armado
    if armado == 0:
        antirrebote.init(period=50, mode=Timer.ONE_SHOT, callback=timer_sw)
        armado = 1

#Inicialización
SW.irq(trigger=Pin.IRQ_FALLING, handler=sw_rsi)
clk_ult = CLK.value()

# Timers
teclado_timer = Timer(0)
teclado_timer.init(mode=Timer.PERIODIC, period=200, callback=rsi)

antirrebote = Timer(1)

encod_timer = Timer(3)
encod_timer.init(mode=Timer.PERIODIC, period=10, callback=rsi_encod)

#Funciones auxiliares
def mostrar_neopixels_estado(pin_usuario, pin_correcto):
    """Muestra en verde los dígitos correctos"""
    for i in range(len(pin_correcto)):
        if pin_usuario[i] == pin_correcto[i]:
            neopixel[i] = (0, 255, 0)  # Verde
        else:
            neopixel[i] = (255, 0, 0)  # Rojo
    neopixel.write()

def pedir_pin(mensaje):
    """Pide un PIN de 6 dígitos usando encoder"""
    pin = [0] * 6
    pos = 0
    print(mensaje)
    while pos < 7:
        if cola:
            evento = cola.pop(0)
            if evento == 'GIROD':
                pin[pos] = (pin[pos] + 1) % 10
            elif evento == 'GIROI':
                pin[pos] = (pin[pos] - 1) % 10
            elif evento == 'SWITCH':
                pos += 1  # Confirma dígito
            print("PIN parcial:", pin)
    return pin

# Programa principal
try:
    # 1. Usuario define PIN
    pin_correcto = pedir_pin("Configura tu PIN (6 dígitos):")
    print("PIN guardado:", pin_correcto)

    # 2. Usuario intenta desbloquear
    pin_ingresado = pedir_pin("Introduce el PIN para desbloquear:")
    mostrar_neopixels_estado(pin_ingresado, pin_correcto)

    # 3. Corrección de dígitos incorrectos
    posicion_digito = 0
    while pin_ingresado != pin_correcto:
        if cola:
            evento = cola.pop(0)
            if evento == 'UP':
                posicion_digito = min((posicion_digito + 1), 5)
            elif evento == 'DOWN':
                posicion_digito = max((posicion_digito - 1), 5)
            elif evento == 'GIROD':
                pin_ingresado[posicion_digito] = (pin_ingresado[posicion_digito] + 1) % 10
            elif evento == 'GIROI':
                pin_ingresado[posicion_digito] = (pin_ingresado[posicion_digito] - 1) % 10
            mostrar_neopixels_estado(pin_ingresado, pin_correcto)
            print("PIN actual:", pin_ingresado)
            print('Te encuentras en el digito: ', posicion_digito)
    # 4. PIN correcto
            
    print("¡CONTRASEÑA CORRECTA!")
    neopixel.fill((0, 255, 0))
    neopixel.write()

except KeyboardInterrupt:
    neopixel.fill((0, 0, 0))
    neopixel.write()
    pass