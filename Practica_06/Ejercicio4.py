#Ejercicio 4
from gpiozero import DigitalOutputDevice 
from time import sleep 
from gpiozero import Device

# Define el pin GPIO que estás usando (en numeración BCM). 
pines = [17,27,22,23,24,25,5,6,13,19]

#Lista con objetos DigitalOutputDevice. 
salidas = [DigitalOutputDevice(pin) for pin in pines]

print("Iniciando secuencia de la salida digital...")

def OFF():
# APAGAR TODOS LEDS
	for salida in salidas:
		salida.off()
	sleep(1)

def ON():
# ENCENDER TODOS LOS LEDS
	for salida in salidas:
		salida.on()
	sleep(1)

def dez_right():
    n = len(salidas)
    
    for i in range(n):
        OFF()
        if i == 0:
            start, end = 0, 1          # Solo LED 0        
        elif i == 1:
            start, end = 0, 2          # LEDs 0 y 1
        elif i == n - 2:
            start, end = n - 3, n      # LEDs 7, 8 y 9 (i=8)
        elif i == n - 1:
            start, end = n - 2, n      # LEDs 8 y 9 (i=9)
        else:
            start = i - 1
            end = i + 2                # 3 LEDs en el medio
        
        for j in range(start, end):
            salidas[j].on()
        sleep(0.5)
    
    # Paso final: solo LED 9
    OFF()
    salidas[n - 1].on()
    sleep(0.5)
    
try:
	OFF()
	ON()
	dez_right()
	OFF()
	ON()

finally:
	
    OFF()
    print("Secuencia finalizada.")
