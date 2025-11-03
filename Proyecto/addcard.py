# addcard.py
from pathlib import Path
import tempfile
import os
import json
import uuid
from datetime import datetime
from filelock import FileLock, Timeout

DB_PATH = Path("db.json")
LOCK_PATH = Path("db.json.lock")
LOCK_TIMEOUT = 5  # segundos

def atomic_write_json(path: Path, data):
    dirpath = path.parent or Path(".")
    with tempfile.NamedTemporaryFile("w", dir=dirpath, delete=False, encoding="utf-8") as tf:
        json.dump(data, tf, ensure_ascii=False, indent=2)
        tmpname = tf.name
    os.replace(tmpname, str(path))

def ensure_db_exists(path: Path):
    if not path.exists():
        atomic_write_json(path, [])

def load_db(path: Path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def find_card_by_serial(db, serial_no):
    serial_no = serial_no.upper()
    for item in db:
        if item.get("serial_no", "").upper() == serial_no:
            return item
    return None

def insert_card_db(db_path: Path, lock_path: Path, serial_no: str, user_id: str) -> bool:
    """
    Intenta insertar la tarjeta (serial_no) con user_id.
    Devuelve True si se insertó, False si ya existía o hubo error.
    """
    serial_no = serial_no.upper()
    ensure_db_exists(db_path)
    lock = FileLock(str(lock_path))

    try:
        with lock.acquire(timeout=LOCK_TIMEOUT):
            db = load_db(db_path)

            if find_card_by_serial(db, serial_no) is not None:
                print(f"[DB] Tarjeta {serial_no} ya existe en la base de datos. Ignorando.")
                return False

            card = {
                "card_id": str(uuid.uuid4()),
                "serial_no": serial_no,
                "user_id": user_id,
                "valid": 1,
                "created_at": datetime.utcnow().isoformat() + "Z"
            }

            db.append(card)
            atomic_write_json(db_path, db)
            print(f"[DB] Tarjeta {serial_no} insertada correctamente.")
            print(json.dumps(card, ensure_ascii=False, indent=2))
            return True
    except Timeout:
        print("[DB][ERROR] No se pudo adquirir el lock del fichero db.json (timeout). Intenta de nuevo.")
        return False
    except Exception as e:
        print(f"[DB][ERROR] Error inesperado al escribir DB: {e}")
        return False
