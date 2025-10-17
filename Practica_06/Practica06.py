from gpiozero import Button
from gpiozero.pins.rpigpio import RPiGPIOFactory
import subprocess
import time

factory = RPiGPIOFactory()

button_pins = {
    'Boton 1': 16,
    'Boton 2': 20,
    'Boton 3': 21,
    'Terminar': 18
}

buttons = {
    name: Button(pin, pull_up=True, pin_factory=factory, bounce_time=0.2)
    for name, pin in button_pins.items()
}

running = True

# Funciones para ejecutar los archivos .py
def ejercicio2():
    print("Ejecutando Ejercicio 2...")
    subprocess.Popen(["python3", "Ejercicio2.py"])

def ejercicio3():
    print("Ejecutando Ejercicio 3...")
    subprocess.Popen(["python3", "Ejercicio3.py"])

def ejercicio4():
    print("Ejecutando Ejercicio 4...")
    subprocess.Popen(["python3", "Ejercicio4.py"])

def boton_presionado(name):
    if name == 'Boton 1':
        ejercicio2()
    elif name == 'Boton 2':
        ejercicio3()
    elif name == 'Boton 3':
        ejercicio4()

def terminar_programa():
    global running
    print("Boton 'Terminar' presionado. Cerrando programa...")
    running = False

for name, button in buttons.items():
    if name == 'Terminar':
        button.when_pressed = terminar_programa
    else:
        button.when_pressed = lambda n=name: boton_presionado(n)

print("Programa iniciado... Presiona los botones (Ctrl+C para salir)")

try:
    while running:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nPrograma finalizado con Ctrl+C.")
finally:
    for button in buttons.values():
        button.close()
    print("GPIO liberados, programa terminado.")
