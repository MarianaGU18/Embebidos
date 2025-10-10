
from gpiozero import DigitalOutputDevice 
from time import sleep 

# Define el pin GPIO que estás usando (en numeración BCM). 
# En lugar de LED, usamos la clase base DigitalOutputDevice. 
salida_digital = DigitalOutputDevice(17) # 17 es el número del GPIO a usar

print("Iniciando secuencia de la salida digital...")

# Bucle que se repetirá 5 veces 
for _ in range(5): 
    print("Salida activada (ON)") 
    salida_digital.on() # Activar la salida (equivale a led.on()) 
    sleep(1) # Esperar 1 segundo 

    print("Salida desactivada (OFF)") 
    salida_digital.off() # Desactivar la salida (equivale a led.off()) 
    sleep(1) # Esperar 1 segundo 

print("Secuencia finalizadda.")
