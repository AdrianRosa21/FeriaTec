# -*- coding: utf-8 -*-
import os

class InterpreteComandos:
    def __init__(self, estado, filesystem):
        self.estado = estado
        self.filesystem = filesystem

    def procesar(self, linea_comando):
        """
        Procesa un comando simulado y actualiza el estado y el sistema de archivos.
        Retorna una tupla: (mensaje_salida, tag_color, requiere_limpiar_pantalla, requiere_salir)
        """
        linea_comando = linea_comando.strip()
        if not linea_comando:
            return "", "normal", False, False

        partes = linea_comando.split()
        cmd_principal = partes[0].lower()
        argumentos = partes[1:] if len(partes) > 1 else []

        # Interceptación de comandos de control de la terminal
        if cmd_principal == "clear":
            return "", "normal", True, False
        elif cmd_principal == "exit":
            return "", "normal", False, True
        elif cmd_principal == "help":
            return self._cmd_help()
        elif cmd_principal == "scan":
            return self._cmd_scan()
        elif cmd_principal == "status":
            return self._cmd_status()
        elif cmd_principal == "logs":
            return self._cmd_logs()
        elif cmd_principal == "processes":
            return self._cmd_processes()
        elif cmd_principal == "inspect":
            return self._cmd_inspect(argumentos)
        elif cmd_principal == "kill":
            return self._cmd_kill(argumentos)
        elif cmd_principal == "clean":
            return self._cmd_clean(argumentos)
        elif cmd_principal == "quarantine":
            return self._cmd_quarantine(argumentos)
        elif cmd_principal == "delete":
            return self._cmd_delete(argumentos)
        elif cmd_principal == "repair":
            return self._cmd_repair(argumentos)
        elif cmd_principal == "restore":
            return self._cmd_restore()
        else:
            # Penalización por comando desconocido
            self.estado.puntuacion = max(0, self.estado.puntuacion - 50)
            return (
                f"[X] ERROR: Comando desconocido: '{cmd_principal}'. Escribe 'help' para ayuda.\n[!] Penalizacion: -50 PTS.\n",
                "error",
                False,
                False
            )

    def _cmd_help(self):
        menu = (
            "=================== COMANDOS DE MITIGACION DISPONIBLES ===================\n"
            "  help                          - Muestra este menu de ayuda.\n"
            "  scan                          - Analiza el sistema simulado.\n"
            "  status                        - Informacion de salud, tiempo y puntuacion.\n"
            "  logs                          - Visualiza registros de auditoria del sistema.\n"
            "  processes                     - Lista los procesos en ejecucion.\n"
            "  inspect <nombre_virus>        - Analiza el ejecutable de la amenaza.\n"
            "  kill <nombre_virus>           - Detiene temporalmente el proceso del virus.\n"
            "  clean temp                    - Elimina archivos temporales infectados.\n"
            "  quarantine <nombre_virus>     - Mueve la amenaza al directorio de cuarentena.\n"
            "  delete <nombre_virus>         - Elimina de forma permanente el archivo de cuarentena.\n"
            "  repair system                 - Repara el sector de arranque y archivos del sistema.\n"
            "  restore                       - Aplica punto de restauracion limpio (Victoria).\n"
            "  clear                         - Limpia el historial de la pantalla.\n"
            "  exit                          - Abandona la simulación.\n"
            "=========================================================================="
        )
        return menu + "\n", "info", False, False

    def _cmd_scan(self):
        # El comando real de análisis lo maneja en parte la app con un retardo visual.
        # Aquí definimos la respuesta semántica.
        self.estado.scan_realizado = True
        return (
            "[OK] Analisis completo finalizado.\n"
            f"[!] Amenaza localizada: '{self.estado.salud_virus * 100:.0f}% - virus.exe.fake' en './simulation_data/'.\n"
            "[!] Archivo temporal potencialmente infectado: './simulation_data/infected_temp.tmp'.\n"
            "[!] Se recomienda ver los 'logs' del sistema para confirmar actividades sospechosas.\n",
            "advertencia",
            False,
            False
        )

    def _cmd_status(self):
        salud_pct = self.estado.obtener_porcentaje_salud()
        tiempo_min = self.estado.tiempo_restante // 60
        tiempo_seg = self.estado.tiempo_restante % 60
        
        # Evaluar el nivel de integridad del sistema simulado
        if salud_pct >= 90:
            integridad = "CRITICO - COMPROMETIDO"
            color = "error"
        elif salud_pct >= 50:
            integridad = "DEBILITADO - EN PROCESO DE CONTENCION"
            color = "advertencia"
        elif salud_pct > 0:
            integridad = "BAJO CONTROL - AMENAZA AISLADA"
            color = "info"
        else:
            integridad = "SEGURO - PENDIENTE DE RESTAURACION"
            color = "normal"

        status_msg = (
            f"=== ESTADO DEL SISTEMA SIMULADO ===\n"
            f"  * Integridad: {integridad}\n"
            f"  * Salud del Virus: {salud_pct}%\n"
            f"  * Puntuacion Actual: {self.estado.puntuacion} PTS\n"
            f"  * Tiempo Restante: {tiempo_min:02d}:{tiempo_seg:02d}\n"
            f"  * Sandbox Seguro: ./simulation_data/\n"
            f"===================================="
        )
        return status_msg + "\n", color, False, False

    def _cmd_logs(self):
        self.estado.logs_vistos = True
        contenido_logs = self.filesystem.leer_logs()
        return (
            "=== REGISTRO DE AUDITORIA (LOGS) ===\n"
            f"{contenido_logs}"
            "====================================\n"
            "[OK] Registros analizados. Recomendacion: ejecuta 'clean temp' para limpiar residuos temporales.\n",
            "normal",
            False,
            False
        )

    def _cmd_processes(self):
        self.estado.procesos_vistos = True
        
        # Muestra una lista de procesos simulados. Si el proceso del virus ya fue matado:
        estado_virus = "SUSPENDED" if self.estado.proceso_muerto else "RUNNING"
        
        proc_list = (
            "=== LISTA DE PROCESOS ACTIVOS ===\n"
            " PID    | PROCESS NAME         | CPU (%) | MEM (MB) | STATUS\n"
            "--------|----------------------|---------|----------|-----------\n"
            " 0004   | System               |  0.1    |   0.5    | RUNNING\n"
            " 0720   | wininit.exe          |  0.0    |   4.2    | RUNNING\n"
            " 1104   | lsass.exe            |  0.2    |  12.8    | RUNNING\n"
            " 3216   | explorer.exe         |  1.5    |  84.1    | RUNNING\n"
        )
        
        if not self.estado.virus_en_cuarentena:
            proc_list += f" 4040   | virus.exe            |  8.7    |  45.3    | {estado_virus}\n"
            
        proc_list += "=================================\n"
        
        if self.estado.proceso_muerto:
            proc_list += "[OK] El proceso virus (PID 4040) esta suspendido. Muevelo con 'quarantine virus'.\n"
        else:
            proc_list += "[WARNING] virus.exe (PID 4040) esta consumiendo recursos de forma anormal.\n"
            
        return proc_list, "advertencia" if not self.estado.proceso_muerto else "info", False, False

    def _cmd_inspect(self, argumentos):
        if not self.estado.scan_realizado:
            self.estado.puntuacion = max(0, self.estado.puntuacion - 50)
            return "[X] ERROR: No puedes inspeccionar una amenaza sin realizar un analisis previo ('scan').\n", "error", False, False

        if not argumentos or argumentos[0] != "virus":
            return "[X] ERROR: Especifica un objetivo valido. Uso: inspect virus\n", "error", False, False

        # Aplicar reducción de salud si es la primera vez
        mensaje = (
            "=== INSPECCION DE LA AMENAZA ===\n"
            "  * Archivo: ./simulation_data/virus.exe.fake\n"
            "  * Tipo: Troyano / Memory Injector Ficticio\n"
            "  * Comportamiento: Inyecta hilos en memoria y corrompe los puntos de restauracion.\n"
            "  * Accion de mitigacion: Detener el proceso con 'kill virus' (requiere PID 4040).\n"
            "=================================\n"
        )
        
        if not self.estado.virus_inspeccionado:
            self.estado.virus_inspeccionado = True
            self.estado.salud_virus = round(self.estado.salud_virus - 0.10, 2)
            self.estado.puntuacion += 100
            mensaje += "[OK] Amenaza inspeccionada. Salud del virus reducida en 10%.\n[+] +100 PTS.\n"
        else:
            mensaje += "[!] La amenaza ya ha sido analizada e inspeccionada.\n"

        return mensaje, "info", False, False

    def _cmd_clean(self, argumentos):
        if not argumentos or argumentos[0] != "temp":
            return "[X] ERROR: Argumento no valido. Uso: clean temp\n", "error", False, False

        # Intentar limpiar
        exito = self.filesystem.limpiar_temporal()
        if exito:
            mensaje = "[OK] Limpiando carpeta temporal de la simulacion...\n[OK] Archivo 'infected_temp.tmp' eliminado exitosamente.\n"
            if not self.estado.temporal_limpiado:
                self.estado.temporal_limpiado = True
                self.estado.salud_virus = round(self.estado.salud_virus - 0.15, 2)
                self.estado.puntuacion += 100
                mensaje += "[OK] Salud del virus reducida en 15%.\n[+] +100 PTS.\n"
            return mensaje, "normal", False, False
        else:
            return "[!] La carpeta temporal ya esta limpia. No se encontro 'infected_temp.tmp'.\n", "advertencia", False, False

    def _cmd_kill(self, argumentos):
        if not self.estado.virus_inspeccionado:
            self.estado.puntuacion = max(0, self.estado.puntuacion - 50)
            return (
                "[X] ERROR: No se puede detener un proceso sin antes inspeccionar sus detalles ('inspect virus').\n"
                "[!] Penalizacion: -50 PTS.\n",
                "error",
                False,
                False
            )

        if not argumentos or argumentos[0] != "virus":
            return "[X] ERROR: Especifica la amenaza a detener. Uso: kill virus\n", "error", False, False

        if self.estado.proceso_muerto:
            return "[!] El proceso del virus ya ha sido detenido (SUSPENDED).\n", "advertencia", False, False

        self.estado.proceso_muerto = True
        self.estado.salud_virus = round(self.estado.salud_virus - 0.20, 2)
        self.estado.puntuacion += 150
        
        mensaje = (
            "[OK] Enviando senal SIGTERM simulada al proceso PID 4040...\n"
            "[OK] Proceso virus.exe detenido temporalmente en memoria.\n"
            "[!] ADVERTENCIA: El archivo ejecutable todavia existe en el disco y puede reiniciarse.\n"
            "[!] Accion requerida: Mueve el archivo a cuarentena usando 'quarantine virus'.\n"
            "[OK] Salud del virus reducida en 20%.\n[+] +150 PTS.\n"
        )
        return mensaje, "info", False, False

    def _cmd_quarantine(self, argumentos):
        if not self.estado.proceso_muerto:
            self.estado.puntuacion = max(0, self.estado.puntuacion - 50)
            return (
                "[X] ERROR: No puedes mover un ejecutable activo a cuarentena. Primero debes detener su proceso ('kill virus').\n"
                "[!] Penalizacion: -50 PTS.\n",
                "error",
                False,
                False
            )

        if not argumentos or argumentos[0] != "virus":
            return "[X] ERROR: Especifica el archivo a aislar. Uso: quarantine virus\n", "error", False, False

        if self.estado.virus_en_cuarentena:
            return "[!] El archivo virus.exe.fake ya se encuentra aislado en la carpeta de cuarentena.\n", "advertencia", False, False

        exito = self.filesystem.mover_a_cuarentena()
        if exito:
            self.estado.virus_en_cuarentena = True
            self.estado.salud_virus = round(self.estado.salud_virus - 0.25, 2)
            self.estado.puntuacion += 200
            mensaje = (
                "[OK] Moviendo 'virus.exe.fake' a la carpeta './simulation_data/quarantine/'.\n"
                "[OK] Archivo aislado con exito del directorio raiz.\n"
                "[!] Se requiere la eliminacion permanente de la amenaza usando 'delete virus'.\n"
                "[OK] Salud del virus reducida en 25%.\n[+] +200 PTS.\n"
            )
            return mensaje, "normal", False, False
        else:
            return "[X] ERROR: No se encontro el archivo 'virus.exe.fake' en el directorio raiz.\n", "error", False, False

    def _cmd_delete(self, argumentos):
        if not self.estado.virus_en_cuarentena:
            self.estado.puntuacion = max(0, self.estado.puntuacion - 50)
            return (
                "[X] ERROR: No puedes eliminar el virus directamente. Primero debes aislarlo en cuarentena ('quarantine virus').\n"
                "[!] Penalizacion: -50 PTS.\n",
                "error",
                False,
                False
            )

        if not argumentos or argumentos[0] != "virus":
            return "[X] ERROR: Uso correcto: delete virus\n", "error", False, False

        if self.estado.virus_eliminado:
            return "[!] El archivo de la amenaza ya fue eliminado permanentemente.\n", "advertencia", False, False

        exito = self.filesystem.eliminar_virus_cuarentena()
        if exito:
            self.estado.virus_eliminado = True
            self.estado.salud_virus = round(self.estado.salud_virus - 0.20, 2)
            self.estado.puntuacion += 150
            mensaje = (
                "[OK] Eliminando permanentemente 'virus.exe.fake' de la cuarentena...\n"
                "[OK] Amenaza erradicada del disco del sandbox.\n"
                "[!] Accion requerida: El sistema de archivos tiene daños remanentes. Ejecuta 'repair system'.\n"
                "[OK] Salud del virus reducida en 20%.\n[+] +150 PTS.\n"
            )
            return mensaje, "normal", False, False
        else:
            return "[X] ERROR: No se pudo localizar el archivo del virus dentro de la cuarentena.\n", "error", False, False

    def _cmd_repair(self, argumentos):
        if not self.estado.virus_eliminado:
            self.estado.puntuacion = max(0, self.estado.puntuacion - 50)
            return (
                "[X] ERROR: No se puede reparar el sistema mientras la amenaza siga activa en el disco. Erradica el virus primero.\n"
                "[!] Penalizacion: -50 PTS.\n",
                "error",
                False,
                False
            )

        if not argumentos or argumentos[0] != "system":
            return "[X] ERROR: Uso correcto: repair system\n", "error", False, False

        if self.estado.sistema_reparado:
            return "[!] El sistema de archivos y puntos de restauracion ya estan en estado VERIFICADO.\n", "advertencia", False, False

        exito = self.filesystem.reparar_sistema()
        if exito:
            # Asegurar que la salud del virus llegue a 0%
            self.estado.sistema_reparado = True
            self.estado.salud_virus = 0.0
            self.estado.puntuacion += 100
            mensaje = (
                "[OK] Iniciando reparacion del registro simulado...\n"
                "[OK] Reconstruyendo base de datos de restauracion './simulation_data/restore_point.json'.\n"
                "[OK] Integridad del sistema simulado: VERIFICADO.\n"
                "[!] Sistema de archivos libre de virus. Listo para restaurar.\n"
                "[!] Accion final: Ejecuta 'restore' para recuperar la configuracion limpia de fabrica.\n"
                "[OK] Salud del virus al 0%.\n[+] +100 PTS.\n"
            )
            return mensaje, "normal", False, False
        else:
            return "[X] ERROR: No se pudo modificar el punto de restauracion. Archivo corrupto o no accesible.\n", "error", False, False

    def _cmd_restore(self):
        if not self.estado.sistema_reparado or self.estado.salud_virus > 0.0:
            self.estado.puntuacion = max(0, self.estado.puntuacion - 100)
            return (
                "[X] ACCESO DENEGADO: El punto de restauracion sigue dañado o el virus sigue activo.\n"
                "[X] REQUISITOS COMPLEMENTARIOS NO CUMPLIDOS. Ejecuta 'repair system' antes de restaurar.\n"
                "[!] Penalizacion grave: -100 PTS.\n",
                "error",
                False,
                False
            )

        # Victoria detectada
        self.estado.juego_activo = False
        self.estado.resultado_final = "VICTORIA"
        return (
            "[OK] Iniciando recuperacion del Punto de Restauracion Seguro...\n"
            "[OK] Deshaciendo cambios simulados del virus...\n"
            "[OK] Reinstalando archivos de sistema virtualizados...\n"
            "[OK] Restauracion completada con exito.\n"
            "==========================================================\n"
            "        SISTEMA SEGURO Y RESTAURADO COMPLETAMENTE\n"
            "==========================================================\n",
            "normal",
            False,
            False
        )
