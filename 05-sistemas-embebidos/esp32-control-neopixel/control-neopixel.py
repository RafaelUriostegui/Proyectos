from machine import ADC, Timer, Pin
from neopixel import NeoPixel
from lcd import LCD

umbral = [0, 600, 1000, 2100, 3000, 4000]
KEYS = ['RIGHT', 'UP', 'DOWN', 'LEFT', 'SELECT', None]

transiciones = ['ESPERA', 'R', 'G', 'B', 'BRILLO:']

estados = {('cambio', 1): 'GIROD', ('cambio', 0): 'GIROI'}

def rsi(timer):
    global cola, teclado, umbral, KEYS
    
    valor_actual = teclado.read()
    for i in range(5, -1, -1):
        if valor_actual >= umbral[i]:
            if i != 5:
                cola.append(KEYS[i])
            break
    
def rsi_encod(timer):
    global clk_ult, movimiento
    clk_act = CLK.value()
    if clk_ult == 1 and clk_act == 0:
        estado_temp = 'cambio'
        movimiento = estados[(estado_temp, DT.value())]
        cola.append(movimiento)
    clk_ult = clk_act

def timer_sw(timer):
    global cuenta, armado, SW
    if SW.value() == 0:
        cuenta = cuenta + 1
        cola.append('SWITCH')
    armado = 0

def sw_rsi(pin):
    global armado
    if armado == 0:
        antirrebote.init(period=ESPERA_ANTIRREBOTE_MS, mode=Timer.ONE_SHOT, callback=timer_sw)
        armado = 1

def actualiza_leds():
    global contador, leds_config
    for i in range(8):
        if transiciones[opciones] == 'ESPERA':
            brillo_actual = brillo_indiv[i] * brillo_global  # global
        else:
            brillo_actual = brillo_indiv[i]  # individual
        neopixel[i] = [int(color * brillo_actual) for color in lista_leds[i]]
    neopixel.write()

CLK = Pin(14, Pin.IN, Pin.PULL_UP)
DT  = Pin(27, Pin.IN, Pin.PULL_UP)
SW  = Pin(13, Pin.IN, Pin.PULL_UP)

SW.irq(trigger=Pin.IRQ_FALLING, handler=sw_rsi)

clk_ult = CLK.value()
click = SW.value()

opciones = 0
leds_config = True
leds_on = True
movimiento = None
brillo_indiv = [1.0 for _ in range(8)]
brillo_global = 1.0
lista_leds = [(0, 0, 0) for _ in range(8)]
cola = []
contador = 0
cuenta = 0

pin_teclado = 34
teclado = ADC(pin_teclado, atten = ADC.ATTN_11DB) #Lectura analogica

pin_neopixel = 33
neopixel = NeoPixel(Pin(pin_neopixel), 8)

teclado_timer = Timer(0)
teclado_timer.init(mode = Timer.PERIODIC, period = 200, callback = rsi)

display = LCD(E=22, RS=4, D7=23, D6=15, D5=21, D4=5)
msj = f'LED {contador + 1}: {transiciones[opciones]}'
display.linea_0(msj)

#Bandera antirrebotes
armado = 0
antirrebote = Timer(1)
ESPERA_ANTIRREBOTE_MS = 20

encod_timer = Timer(3)
encod_timer.init(mode=Timer.PERIODIC, period=10, callback=rsi_encod)


try:
    while True:
        if len(cola) > 0:
            tecla = cola.pop(0)
            
            if tecla == 'SELECT':
                leds_config = not leds_config
            elif tecla == 'UP' and leds_config:
                contador = min(contador + 1, 7)
                opciones = 0
            elif tecla == 'DOWN' and leds_config:
                contador = max(contador - 1, 0)
                opciones = 0
            elif tecla == 'RIGHT':
                leds_config = False
                opciones = min(opciones + 1, 4)
            elif tecla == 'LEFT':
                leds_config = False
                opciones = max(opciones - 1, 0)               
            elif tecla in ['GIROD', 'GIROI']:
                if transiciones[opciones] == 'R':
                    r, g, b = lista_leds[contador]
                    step = 5 if tecla == 'GIROD' else -5
                    r = max(0, min(255, r + step))
                    lista_leds[contador] = (r, g, b)
                    
                elif transiciones[opciones] == 'G':
                    r, g, b = lista_leds[contador]
                    step = 5 if tecla == 'GIROD' else -5
                    g = max(0, min(255, g + step))
                    lista_leds[contador] = (r, g, b)
                
                elif transiciones[opciones] == 'B':
                    r, g, b = lista_leds[contador]
                    step = 5 if tecla == 'GIROD' else -5
                    b = max(0, min(255, b + step))
                    lista_leds[contador] = (r, g, b)
                
                elif transiciones[opciones] == 'BRILLO:':
                    if tecla == 'GIROD':
                        brillo_indiv[contador] = min(brillo_indiv[contador] + 0.1, 1.0)
                    elif tecla == 'GIROI':
                        brillo_indiv[contador] = max(brillo_indiv[contador] - 0.1, 0.0)
                    
                elif transiciones[opciones] == 'ESPERA':
                    if tecla == 'GIROD':
                        brillo_global = min(brillo_global + 0.1, 1.0)
                    elif tecla == 'GIROI':
                        brillo_global = max(brillo_global - 0.1, 0.0)
            elif tecla == 'SWITCH':
                leds_on = not leds_on
                if leds_on:
                    brillo_global = brillo_mem  #Restaura el brillo
                else:
                    brillo_mem = brillo_global  #Lo guarda antes de apagar
                    brillo_global = 0.0         #Apagar
            
            if tecla == 'SELECT':
                msj = f'LED {contador + 1}: LISTO'
                display.linea_0(msj)
            else:
                msj = f'LED {contador + 1}: {transiciones[opciones]}'
                display.linea_0(msj)    
                msj = f'{lista_leds[contador]} {brillo_indiv[contador] * 100}'
                display.linea_1(msj)
                if transiciones[opciones] == 'BRILLO:':
                    msj = f'{lista_leds[contador]} {int(brillo_indiv[contador]*100)}'
                    display.linea_1(msj)
                elif transiciones[opciones] == 'ESPERA':
                    if tecla == 'GIROD':
                        msj = f'Brillo global:{int(brillo_global*100)}%'
                        display.linea_1(msj)
                    elif tecla == 'GIROI':
                        msj = f'Brillo global:{int(brillo_global*100)}%'
                        display.linea_1(msj)
                    elif tecla == 'SWITCH' and not leds_on:
                        display.limpia()
                        msj = f' MODO DE LEDS:'
                        display.linea_0(msj)
                        msj = f'    APAGADO'
                        display.linea_1(msj)
            actualiza_leds()
            
except KeyboardInterrupt:
    for i in range(8):
        neopixel[i] = (0, 0, 0)
    neopixel.write()
    display.limpia()
    pass