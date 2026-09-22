# ESP32 — Cerradura electrónica con PIN

> **EN —** An electronic PIN lock on ESP32/MicroPython. The rotary encoder changes the digit under the
> cursor while the keypad moves between positions and confirms, so a full PIN can be entered and
> edited with one encoder and five buttons. The NeoPixel strip gives the user feedback on entry,
> success and failure.

## Objetivo

Implementar una cerradura que permita **capturar y editar un PIN** con una interfaz mínima: un encoder
rotatorio y un teclado analógico de cinco botones.

## Interacción

- El **encoder** incrementa o decrementa el dígito en la posición actual.
- Las teclas `LEFT` / `RIGHT` mueven el cursor entre posiciones del PIN, lo que permite **corregir un
  dígito ya introducido** sin empezar de nuevo.
- `SELECT` confirma y valida contra el PIN correcto.
- La **tira NeoPixel** indica el estado: posición en edición, acierto y fallo.

## Detalles de implementación

Comparte la base técnica del [control de NeoPixel](../esp32-control-neopixel/) — teclado analógico por
umbrales ADC, lectura del encoder por flanco, antirrebote con temporizador *one-shot* y arquitectura
por cola de eventos — aplicada aquí a la lógica de una cerradura con estado.

## Hardware

| Componente | Conexión |
|---|---|
| Teclado analógico | ADC en GPIO 34 (atenuación 11 dB) |
| Encoder `CLK` / `DT` / `SW` | GPIO 14 / 27 / 13, con *pull-up* |
| Tira NeoPixel (8 LED) | GPIO 33 |

## Stack

**MicroPython** sobre **ESP32** — `machine.ADC`, `machine.Timer`, `machine.Pin`, `neopixel.NeoPixel`

## Cómo ejecutar

Requiere MicroPython en el ESP32. Cargar con `ampy`, `rshell` o Thonny.

---

<sub>Proyecto libre de Señales y Medición (SyM) — UAM, trimestre 25-P.</sub>
