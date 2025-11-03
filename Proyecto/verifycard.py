# Tag/verifycard.py

import signal
import time
from pathlib import Path
import json
from readcard import RFIDReader  # Import absoluto desde el paquete Tag

DB_PATH = Path("db.json")

class RFIDVerifier:
    """
    Clase que encapsula la verificación de tarjetas RFID con DB JSON.
    """

    def __init__(self, db_path: Path = None, debounce_seconds: float = 2.0):
        self.db_path = db_path or DB_PATH
        self.reader = RFIDReader(debounce_seconds=debounce_seconds)
        self.continue_reading = True

        # Configurar Ctrl+C
        signal.signal(signal.SIGINT, self._end_read)

    def _end_read(self, signal_received, frame):
        """Maneja Ctrl+C para detener el loop"""
        print("\n[SYS] Ctrl+C detectado — finalizando...")
        self.continue_reading = False

    def verify_card_db(self, serial_no: str):
        """
        Devuelve el user_id si la tarjeta existe en la DB, None si no.
        """
        serial_no = serial_no.upper()
        if not self.db_path.exists():
            return None

        with self.db_path.open("r", encoding="utf-8") as f:
            try:
                db = json.load(f)
            except json.JSONDecodeError:
                return None

        for item in db:
            if item.get("serial_no", "").upper() == serial_no:
                return item.get("user_id")
        return None

    def poll_once(self):
        """Lee una tarjeta una vez y devuelve user_id si existe, None si no."""
        serial = self.reader.read_once()
        if serial:
            user_id = self.verify_card_db(serial)
            return serial, user_id
        return None, None

    def poll_forever(self, callback=None, poll_interval: float = 0.1):
        """
        Lee tarjetas continuamente hasta detenerse.
        callback: función opcional que recibe (serial, user_id)
        """
        print("Iniciando lector. Acerca una tarjeta... (Ctrl+C para salir)\n")
        self.continue_reading = True
        while self.continue_reading:
            try:
                serial, user_id = self.poll_once()
                if serial:
                    if user_id:
                        print(f"[RFID] Card read UID: {serial} -> ✅ Bienvenido, {user_id}!")
                    else:
                        print(f"[RFID] Card read UID: {serial} -> ❌ Tarjeta no registrada")
                    if callback:
                        callback(serial, user_id)
                time.sleep(poll_interval)
            except Exception as e:
                print(f"[ERROR] Excepción en poll_forever: {e}")
                time.sleep(0.5)
