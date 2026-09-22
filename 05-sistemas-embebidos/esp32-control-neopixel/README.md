# ESP32 — Control de NeoPixel con teclado analógico y encoder

> **EN —** MicroPython firmware for an ESP32 driving an 8-LED NeoPixel strip and an LCD. Input comes
> from an analogue keypad read on a single ADC pin by voltage thresholds and from a rotary encoder
> with a push switch. Everything is event-driven: ISRs push events into a queue that the main loop
> consumes, and the switch is debounced with a one-shot timer.

## Lo que resuelve

### Teclado analógico en un solo pin ADC

Cinco botones comparten una única entrada analógica mediante un divisor resistivo. La rutina de
servicio lee el ADC y compara contra una tabla de umbrales **recorriéndola de mayor a menor**, que es
lo que hace la discriminación fiable:

```python
umbral = [0, 600, 1000, 2100, 3000, 4000]
KEYS = ['RIGHT', 'UP', 'DOWN', 'LEFT', 'SELECT', None]
```

### Encoder rotatorio con detección de sentido

El sentido de giro se deduce del estado del pin `DT` en el **flanco de bajada** de `CLK`, resuelto con
un diccionario de transición de estados en lugar de condicionales anidados:

```python
estados = {('cambio', 1): 'GIROD', ('cambio', 0): 'GIROI'}
```

### Antirrebote por temporizador *one-shot*

El botón del encoder no se lee directamente en la interrupción. La ISR arma un `Timer.ONE_SHOT` y es
el temporizador quien confirma el estado del pin cuando el rebote mecánico ya terminó — evita las
pulsaciones múltiples espurias sin bloquear con `sleep`.

### Arquitectura por eventos

Ninguna ISR hace trabajo pesado: todas encolan un evento y retornan de inmediato. El bucle principal
consume la cola y avanza la **máquina de estados** (`ESPERA → R → G → B → BRILLO`), que determina qué
componente de color o qué brillo modifica el encoder en cada momento.

## Hardware

| Componente | Conexión |
|---|---|
| Teclado analógico | ADC en GPIO 34 (atenuación 11 dB) |
| Encoder `CLK` / `DT` / `SW` | GPIO 14 / 27 / 13, con *pull-up* |
| Tira NeoPixel (8 LED) | GPIO 33 |
| LCD | vía módulo `lcd` |

## Stack

**MicroPython** sobre **ESP32** — `machine.ADC`, `machine.Timer`, `machine.Pin`, `neopixel.NeoPixel`

## Cómo ejecutar

Requiere MicroPython en el ESP32 y los módulos `lcd` y `neopixel` en el sistema de archivos del
dispositivo. Cargar con `ampy`, `rshell` o Thonny.

---

<sub>Proyecto final de Señales y Medición (SyM) — UAM, trimestre 25-P.</sub>
