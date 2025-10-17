import time
from RPLCD.i2c import CharLCD

#uso de la direccion I2C  definiendo que la pantalla LCD es de 16 columnas por 2 filas
i2c_address = 0x27
lcd = CharLCD(i2c_expander='PCF8574', address=i2c_address, port=1, cols=16, rows=2, dotsize=8) 

#se borra el contenido de la pantalla
lcd.clear()

#Mostrar el primer mensaje
lcd.write_string("   FSE 2026-1   ")
lcd.crlf()
lcd.write_string("BRIGADA03 GPO.04")
time.sleep(3)  # Aumentar el tiempo de espera

# Mostrar el segundo mensaje
lcd.clear()
lcd.write_string("Esteban Tonatiuh")
lcd.crlf()
lcd.write_string("Caudillo Aviles")
time.sleep(3)  # Aumentar el tiempo de espera

# Mostrar el tercer mensaje
lcd.clear()
lcd.write_string("Juan Jose")
lcd.crlf()
lcd.write_string("Lopez Rangel")
time.sleep(3)  # Aumentar el tiempo de espera

# Mostrar el cuarto mensaje
lcd.clear()
lcd.write_string("Eduardo")
lcd.crlf()
lcd.write_string("Zavala Sanchez")
time.sleep(3)  # Aumentar el tiempo de espera



# Mostrar el quinto mensaje
lcd.clear()
lcd.write_string("Mariana")
lcd.crlf()
lcd.write_string("Gomez Urbano")
time.sleep(3)  # Aumentar el tiempo de espe
# Limpiar la pantalla y cerrar el LCD al finalizar
lcd.clear()
lcd.close()

