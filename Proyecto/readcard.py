# readcard.py
import time

# Asegúrate de tener instalada la librería MFRC522 adecuada en tu RPi
import MFRC522

class RFIDReader:
    def __init__(self, debounce_seconds: float = 2.0):
        self.reader = MFRC522.MFRC522()
        self.debounce_seconds = debounce_seconds
        self._last_seen = None
        self._last_seen_time = 0

    def uid_to_string(self, uid):
        s = ""
        for i in uid:
            s = format(i, "02X") + s
        return s

    def read_once(self):
        """
        Intenta detectar una tarjeta: si encuentra una distinta (o pasada la ventana de debounce)
        devuelve la serial en mayúsculas; si no hay tarjeta o es la misma dentro del debounce, devuelve None.
        """
        try:
            (status, TagType) = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
            if status == self.reader.MI_OK:
                (status2, uid) = self.reader.MFRC522_SelectTagSN()
                if status2 == self.reader.MI_OK:
                    serial = self.uid_to_string(uid)
                    now = time.time()
                    if serial == self._last_seen and (now - self._last_seen_time) < self.debounce_seconds:
                        # misma tarjeta, dentro del debounce -> ignoramos
                        return None
                    # nueva tarjeta o fuera de debounce
                    self._last_seen = serial
                    self._last_seen_time = now
                    return serial
                else:
                    # error de autenticación / lectura
                    return None
            else:
                return None
        except Exception as e:
            # propaga la excepción al llamador o devuelve None según prefieras
            raise

    def poll_forever(self, callback, poll_interval: float = 0.1):
        """
        Llama a callback(serial) cada vez que se detecte una tarjeta válida.
        callback debe aceptar un argumento: serial (str).
        """
        try:
            while True:
                serial = self.read_once()
                if serial:
                    callback(serial)
                time.sleep(poll_interval)
        except KeyboardInterrupt:
            # dejar que el llamador cierre
            return
