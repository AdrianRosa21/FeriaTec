# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import json
import threading

class RankingClient:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def enviar_puntuacion_async(self, nombre, puntuacion, tiempo_restante, resultado, password, callback=None):
        """
        Envía la puntuación al servidor en un hilo secundario para evitar congelar la interfaz gráfica.
        """
        thread = threading.Thread(
            target=self._ejecutar_peticion,
            args=(nombre, puntuacion, tiempo_restante, resultado, password, callback),
            daemon=True
        )
        thread.start()

    def _ejecutar_peticion(self, nombre, puntuacion, tiempo_restante, resultado, password, callback):
        payload = {
            "player_name": nombre,
            "score": puntuacion,
            "time_left": tiempo_restante,
            "status": resultado,
            "password": password
        }
        
        datos = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.api_url, data=datos, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Bearer {self.api_key}")
        
        exito = False
        mensaje_error = ""

        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 201 or response.status == 200:
                    exito = True
                else:
                    mensaje_error = f"Código de estado HTTP: {response.status}"
        except urllib.error.HTTPError as e:
            mensaje_error = f"Error HTTP {e.code}: {e.reason}"
        except urllib.error.URLError as e:
            mensaje_error = f"Error de red/servidor: {e.reason}"
        except Exception as e:
            mensaje_error = f"Error inesperado: {str(e)}"

        if callback:
            callback(exito, mensaje_error)
