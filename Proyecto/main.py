# main.py

import signal
from auth import setup_master_code, verify_master_code
from modes import mode_verify
from menu import open_menu

# Variable global para controlar el bucle principal
continue_reading = True

def stop_flag():
    """Funcion que devuelve el estado de ejecucion para detener los bucles."""
    return continue_reading

def end_read(signal_received, frame):
    """Manejador de Ctrl+C para detener el programa de forma segura."""
    global continue_reading
    print("\n[SYS] Ctrl+C detectado, finalizando...")
    continue_reading = False

# Registrar el manejador de senales
signal.signal(signal.SIGINT, end_read)

def main():
    global continue_reading

    # Configura o carga el codigo maestro
    master_code = setup_master_code()

    print("\n=== Sistema RFID Activo (arranca en modo verificacion) ===")
    print("Para acceder al menu protegido escribe '0000' y presiona Enter. Se solicitara codigo maestro.")

    # Ejecuta el modo verificacion
    mode_verify(
        stop_flag=stop_flag,       # Funcion para verificar si se debe continuar
        allow_menu=True,           # Permite abrir el menu desde la verificacion
        master_code=master_code,   # Codigo maestro cargado
        open_menu_func=open_menu   # Funcion de menu que se ejecuta al ingresar el master code
    )

    print("[SYS] Sistema cerrado. Adios~")

if __name__ == "__main__":
    main()
