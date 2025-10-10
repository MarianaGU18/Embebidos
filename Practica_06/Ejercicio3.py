#Ejercicio 3
from gpiozero import DigitalOutputDevice 
from time import sleep 

# Define el pin GPIO que estás usando (en numeración BCM). 
pines = [17,27,22,23,24,25,5,6,13,19]

#Lista con objetos DigitalOutputDevice. 
salidas = [DigitalOutputDevice(pin) for pin in pines]

print("Iniciando secuencia de la salida digital...")

# Bucle que se repetirá 5 veces 

for _ in range(5):
    print("Salidas activadas (ON)")
    for salida in salidas:
        salida.on()  # Encender cada salida
    sleep(1)

    print("Salidas desactivadas (OFF)")
    for salida in salidas:
        salida.off()  # Apagar cada salida
    sleep(1)

print("Secuencia finalizada.")
