# db_utils.py
import json
from pathlib import Path
from addcard import DB_PATH  # viene de tu addcard.py

def verify_card(serial_no):
    """Verifica si una tarjeta está en la DB y devuelve el usuario."""
    if not DB_PATH.exists():
        return None
    with DB_PATH.open("r", encoding="utf-8") as f:
        try:
            db = json.load(f)
        except json.JSONDecodeError:
            return None
    for item in db:
        if item.get("serial_no", "").upper() == serial_no.upper():
            return item.get("user_id")
    return None

