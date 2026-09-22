# Sistemas embebidos

> **EN —** ESP32 firmware in MicroPython. Both projects share an event-driven architecture: interrupt
> service routines only enqueue events, a one-shot timer handles switch debouncing, and five buttons
> are multiplexed onto a single ADC pin by voltage thresholds.

Firmware para ESP32 en MicroPython, con arquitectura por eventos e interrupciones.

| Proyecto | Descripción | Stack |
|---|---|---|
| [Control de NeoPixel](esp32-control-neopixel/) | Máquina de estados con teclado analógico, encoder rotatorio, antirrebote por temporizador y control de tira NeoPixel + LCD | MicroPython, ESP32 |
| [Cerradura con PIN](esp32-cerradura-pin/) | Captura y edición de PIN con encoder y teclado, con realimentación visual por NeoPixel | MicroPython, ESP32 |

## Técnicas compartidas

- **Teclado analógico en un solo pin ADC**: cinco botones discriminados por umbrales de voltaje,
  recorriendo la tabla de mayor a menor.
- **Encoder rotatorio**: sentido de giro deducido del estado de `DT` en el flanco de bajada de `CLK`,
  resuelto con un diccionario de transiciones.
- **Antirrebote por `Timer.ONE_SHOT`**: la ISR arma un temporizador y es este quien confirma el
  estado del pin, sin bloquear con `sleep`.
- **Cola de eventos**: ninguna rutina de interrupción hace trabajo pesado; el bucle principal consume
  la cola.

> Estos proyectos corren en hardware, no en el equipo local: requieren un ESP32 con MicroPython.
