from gpiozero import Device, DigitalOutputDevice, Button
from time import sleep

# Pines BCM de las filas y columnas de tu keypad 4x4
rows_pins = [5, 6, 13, 19]
cols_pins = [26, 20, 21, 4]

# Mapa de teclas
keys = [
    "1", "2", "3", "A",
    "4", "5", "6", "B",
    "7", "8", "9", "C",
    "*", "0", "#", "D"
]

# Configurar filas como salidas y columnas como botones
rows = [DigitalOutputDevice(pin) for pin in rows_pins]
cols = [Button(pin, pull_up=False) for pin in cols_pins]

# Funcion para leer las teclas presionadas
def read_keypad():
    pressed = []
    for i, row in enumerate(rows):
        row.on()
        for j, col in enumerate(cols):
            if col.is_pressed:
                pressed.append(keys[i * 4 + j])
        row.off()
    return pressed

# Funcion para liberar pines
def liberar_pines():
    for r in rows: r.close()
    for c in cols: c.close()
    
    
def get_code():
    last_pressed = []
    current_input = ""  # Aqui guardamos lo que se va escribiendo
    print("==================================")
    print("ESCRIBE TU TEXTO EN EL KEYPAD")
    print("Presiona '*' para cancelar, '#' para confirmar")
    print("==================================")

    try:
        while True:
            pressed_keys = read_keypad()
            # Filtrar solo teclas nuevas
            new_keys = [k for k in pressed_keys if k not in last_pressed]

            for key in new_keys:
                if key == "*":  # Cancelar / salir
                    print("Cancelado. Limpiando entrada...")
                    current_input = ""
                    return ""  # Retorna vaco si se cancela
                elif key == "#":  # Confirmar
                    print(f"\nEntrada confirmada: {current_input}")
                    return current_input  # Devuelve la entrada actual cuando se confirma
                else:
                    current_input += key
                    print(f"\r{current_input}", end="", flush=True)

            last_pressed = pressed_keys
            sleep(0.1)

    except KeyboardInterrupt:
        print("Liberando pines por interrupcion")
        liberar_pines()
        return ""
    
"""
def get_code():
    last_pressed = []
    current_input = ""  # Aqui guardamos lo que se va escribiendo
    print("==================================")
    print("ESCRIBE TU TEXTO EN EL KEYPAD")
    print("Presiona '*' para cancelar, '#' para confirmar")
    print("==================================")

    try:
        while True:
            pressed_keys = read_keypad()
            # Filtrar solo teclas nuevas
            new_keys = [k for k in pressed_keys if k not in last_pressed]

            for key in new_keys:
                if key == "*":  # Cancelar / salir
                    print("Cancelado. Limpiando entrada...")
                    current_input = ""
                    return
                elif key == "#":  # Enter / confirmar
                    print(f"Entrada confirmada: {current_input}")
                    current_input = ""  # Reiniciar despues de confirmar
                else:
                    current_input += key
                    print(f"\r{current_input}", end="", flush=True)


            last_pressed = pressed_keys
            sleep(0.1)

    except KeyboardInterrupt:
        print("Liberando pines por interrupcion")
        liberar_pines()
"""
