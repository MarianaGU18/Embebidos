# modes.py
import sys
import select
import time
import json

from readcard import RFIDReader
from addcard import insert_card_db, DB_PATH, LOCK_PATH
from db_utils import verify_card
from addcard import atomic_write_json  # si existe en addcard
from auth import verify_master_code
from stepMotor.motor import motor

def mode_register(user_id, stop_flag):
    reader = RFIDReader(debounce_seconds=2.0)
    print("Acerca una tarjeta para registrar...")
    while stop_flag():
        serial = reader.read_once()
        if serial:
            print(f"[RFID] Card read UID: {serial}")
            inserted = insert_card_db(DB_PATH, LOCK_PATH, serial, user_id)
            if inserted:
                print("[SYS] Registro completado. Salir del modo registrar.")
                break
        time.sleep(0.1)

def mode_delete(stop_flag):
    reader = RFIDReader(debounce_seconds=0.5)
    print("Modo eliminacin activo. Acerca una tarjeta a eliminar...")
    last_uid = None
    while stop_flag(): 
        serial = reader.read_once()
        if serial and serial != last_uid:
            last_uid = serial
            user = verify_card(serial)
            if user:
                print(f"? Bienvenido, {user}! Tarjeta verificada correctamente.")
            else:
                print("? Tarjeta no registrada.")

            if DB_PATH.exists():
                with DB_PATH.open("r", encoding="utf-8") as f:
                    try:
                        db = json.load(f)
                    except json.JSONDecodeError:
                        continue

                new_db = [item for item in db if item.get("serial_no","").upper() != serial.upper()]
                if len(new_db) != len(db):
                    atomic_write_json(DB_PATH, new_db)
                    print(f"[DB] Tarjeta {serial} eliminada automticamente.")

            print("[SYS] Volviendo al men...")
            break

        elif serial is None:
            last_uid = None

        time.sleep(0.1)


def mode_verify(stop_flag, allow_menu=True, master_code=None, open_menu_func=None):
    """
    stop_flag: funcion que retorna True mientras el programa deba seguir leyendo
    """
    reader = RFIDReader(debounce_seconds=2.0)
    print("Modo verificacion activo. Acerca tarjetas... (escribe '0000' + Enter para menu)")

    while stop_flag():
        serial = reader.read_once()
        if serial:
            user = verify_card(serial)
            if user:
                print(f"? Bienvenido, {user}! Tarjeta verificada correctamente.")
                motor()
            else:
                print("? Tarjeta no registrada.")

        if allow_menu:
            dr, _, _ = select.select([sys.stdin], [], [], 0.1)
            if dr:
                cmd = sys.stdin.readline().strip()
                if cmd.lower() == '0000':
                    if master_code and verify_master_code(master_code):
                        if open_menu_func:
                            open_menu_func(master_code, stop_flag)
                        print("Volviendo al modo verificacion...")
                    else:
                        print("[SYS] Codigo maestro incorrecto. Volviendo a verificacion.")
        else:
            time.sleep(0.1)
