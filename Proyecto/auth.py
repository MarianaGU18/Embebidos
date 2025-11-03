import json
from pathlib import Path

MASTER_CODE_FILE = Path("master_code.json")

def setup_master_code():
    """Solicita y guarda el codigo maestro la primera vez."""
    if MASTER_CODE_FILE.exists():
        with MASTER_CODE_FILE.open("r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return data.get("master_code")
            except json.JSONDecodeError:
                pass

    while True:
        code = input("Configura el codigo maestro (ej: 2002): ").strip()
        if code:
            MASTER_CODE_FILE.write_text(json.dumps({"master_code": code}), encoding="utf-8")
            print("[SYS] Codigo maestro guardado.")
            return code
        print("[SYS] Codigo invalido, intenta de nuevo.")

def verify_master_code(stored_code):
    """Solicita el codigo y verifica si es correcto."""
    attempt = input("Ingresa el codigo maestro para acceder: ").strip()
    return attempt == stored_code
