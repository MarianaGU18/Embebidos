from modes import mode_register, mode_delete
from addcard import DB_PATH, LOCK_PATH
import os
import signal

def open_menu(master_code, stop_flag):
    """Menu protegido; usa input() internamente y puede detener el programa llamando stop_callback()."""
    while stop_flag():
        print("\n=== MENU PROTEGIDO ===")
        print("1. Registrar tarjeta")
        print("2. Eliminar tarjeta")
        print("3. Volver a modo verificacion")
        print("4. Terminar programa")
        choice = input("Selecciona opcion (1/2/3/4): ").strip()

        if choice == "1":
            user_id = input("Nombre de usuario para asociar a la tarjeta: ").strip()
            if user_id:
                mode_register(user_id, stop_flag)
        elif choice == "2":
            mode_delete(stop_flag)
        elif choice == "3":
            print("[SYS] Regresando al modo verificacion...")
            break
        elif choice == "4":
            print("[SYS] Saliendo del sistema...")
            os.kill(os.getpid(), signal.SIGINT)
            return "exit"
        else:
            print("[SYS] Opcion invalida. Intenta de nuevo.")
    return None
