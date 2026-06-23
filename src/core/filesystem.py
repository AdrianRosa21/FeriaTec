# -*- coding: utf-8 -*-
import os
import shutil
import json

class SandboxFilesystem:
    def __init__(self):
        # Determinar ruta base absoluta de simulation_data en la raíz del proyecto
        self.ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "simulation_data"))
        self.ruta_cuarentena = os.path.join(self.ruta_raiz, "quarantine")
        self.inicializar_sandbox()

    def es_ruta_segura(self, ruta):
        # Comprobar que la ruta absoluta resuelta esté dentro de la raíz del sandbox
        ruta_absoluta = os.path.abspath(ruta)
        return ruta_absoluta.startswith(self.ruta_raiz)

    def inicializar_sandbox(self):
        # Crear directorios principales
        os.makedirs(self.ruta_raiz, exist_ok=True)
        os.makedirs(self.ruta_cuarentena, exist_ok=True)

        # 1. Crear virus.exe.fake (Ficticio e inofensivo)
        ruta_virus = os.path.join(self.ruta_raiz, "virus.exe.fake")
        if not os.path.exists(ruta_virus):
            with open(ruta_virus, "w", encoding="utf-8") as f:
                f.write("[!] CYBER RESCUE SIMULATION - ARCHIVO DE SIMULACION CONTROLADO - INOFENSIVO\n")
                f.write("PROCESO_PID: 4040\nSTATUS: RUNNING\n")

        # 2. Crear infected_temp.tmp
        ruta_temp = os.path.join(self.ruta_raiz, "infected_temp.tmp")
        if not os.path.exists(ruta_temp):
            with open(ruta_temp, "w", encoding="utf-8") as f:
                f.write("TEMP_FILE_DATA_BLOCK_A98F77B\n")
                f.write("CONTAMINATED_BY_VIRUS: TRUE\n")

        # 3. Crear system_logs.txt
        ruta_logs = os.path.join(self.ruta_raiz, "system_logs.txt")
        # Siempre sobreescribimos los logs al inicio para tener un estado fresco
        with open(ruta_logs, "w", encoding="utf-8") as f:
            f.write("SYSTEM AUDIT LOGS - SECURE OS SIMULATION\n")
            f.write("========================================\n")
            f.write("[INFO] 2026-06-20 21:00:01 - Servicio de red inicializado correctamente.\n")
            f.write("[WARNING] 2026-06-20 21:05:14 - Archivo temporal sospechoso detectado en ./simulation_data/infected_temp.tmp\n")
            f.write("[WARNING] 2026-06-20 21:05:15 - virus detectado intentando inyectar codigo en memoria virtual.\n")
            f.write("[INFO] 2026-06-20 21:10:00 - Alerta de integridad del sistema activada.\n")

        # 4. Crear restore_point.json
        ruta_restore = os.path.join(self.ruta_raiz, "restore_point.json")
        with open(ruta_restore, "w", encoding="utf-8") as f:
            datos_restauracion = {
                "nombre_punto": "Punto de Restauracion Seguro de Fabrica",
                "estado_integridad": "CORRUPTO",
                "detalles": "Faltan firmas del sistema. Se requiere eliminar virus y reparar el sistema antes de restaurar.",
                "reparado": False
            }
            json.dump(datos_restauracion, f, indent=4, ensure_ascii=False)

    def reiniciar_sandbox(self):
        # Eliminar y recrear todo el directorio simulation_data
        if os.path.exists(self.ruta_raiz):
            try:
                shutil.rmtree(self.ruta_raiz)
            except Exception:
                pass
        self.inicializar_sandbox()

    def leer_logs(self):
        ruta_logs = os.path.join(self.ruta_raiz, "system_logs.txt")
        if self.es_ruta_segura(ruta_logs) and os.path.exists(ruta_logs):
            with open(ruta_logs, "r", encoding="utf-8") as f:
                return f.read()
        return "[X] No se puede leer el archivo de registros de auditoria.\n"

    def limpiar_temporal(self):
        ruta_temp = os.path.join(self.ruta_raiz, "infected_temp.tmp")
        if self.es_ruta_segura(ruta_temp) and os.path.exists(ruta_temp):
            os.remove(ruta_temp)
            return True
        return False

    def mover_a_cuarentena(self):
        ruta_virus = os.path.join(self.ruta_raiz, "virus.exe.fake")
        ruta_destino = os.path.join(self.ruta_cuarentena, "virus.exe.fake")
        
        if self.es_ruta_segura(ruta_virus) and self.es_ruta_segura(ruta_destino):
            if os.path.exists(ruta_virus):
                shutil.move(ruta_virus, ruta_destino)
                return True
        return False

    def eliminar_virus_cuarentena(self):
        ruta_destino = os.path.join(self.ruta_cuarentena, "virus.exe.fake")
        if self.es_ruta_segura(ruta_destino) and os.path.exists(ruta_destino):
            os.remove(ruta_destino)
            return True
        return False

    def reparar_sistema(self):
        ruta_restore = os.path.join(self.ruta_raiz, "restore_point.json")
        if self.es_ruta_segura(ruta_restore) and os.path.exists(ruta_restore):
            try:
                with open(ruta_restore, "r+", encoding="utf-8") as f:
                    datos = json.load(f)
                    datos["estado_integridad"] = "VERIFICADO"
                    datos["detalles"] = "El sistema de archivos simulado esta limpio y listo para restauracion."
                    datos["reparado"] = True
                    f.seek(0)
                    json.dump(datos, f, indent=4, ensure_ascii=False)
                    f.truncate()
                return True
            except Exception:
                return False
        return False

    def verificar_estado_archivos(self):
        # Devuelve un diccionario con el estado actual de los archivos reales en el sandbox
        return {
            "virus_raiz_existe": os.path.exists(os.path.join(self.ruta_raiz, "virus.exe.fake")),
            "temp_existe": os.path.exists(os.path.join(self.ruta_raiz, "infected_temp.tmp")),
            "virus_cuarentena_existe": os.path.exists(os.path.join(self.ruta_cuarentena, "virus.exe.fake")),
            "reparado_ok": self._verificar_reparado_json()
        }

    def _verificar_reparado_json(self):
        ruta_restore = os.path.join(self.ruta_raiz, "restore_point.json")
        if os.path.exists(ruta_restore):
            try:
                with open(ruta_restore, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    return datos.get("reparado", False)
            except Exception:
                return False
        return False
