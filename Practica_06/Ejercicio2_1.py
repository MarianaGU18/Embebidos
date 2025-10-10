from gpiozero import LED 
from time import sleep 

# Define el pin GPIO que estas usando (en numeracion BCM). 
# El pin 17 es una opcion comun para empezar. 
led = LED(17) 

print("Iniciando secuencia del LED...") 
# Bucle que se repetira 5 veces
for _ in range(5): 
	print("LED encendido") 
	led.on() # Encender el LED 
	sleep(1) # Esperar 1 segundo
	 
	print("LED apagado") 
	led.off() # Apagar el LED 
	sleep(1) # Esperar 1 segundo 
print("Secuencia finalizada.")
