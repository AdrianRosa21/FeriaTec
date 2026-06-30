# -*- coding: utf-8 -*-
import os

class InterpreteComandosFacil:
    def __init__(self, estado, filesystem):
        self.estado = estado
        self.filesystem = filesystem

    def procesar(self, linea_comando):
        linea_comando = linea_comando.strip()
        if not linea_comando:
            return "", "normal", False, False

        partes = linea_comando.split()
        cmd_principal = partes[0].lower()

        if cmd_principal == "clear":
            return "", "normal", True, False
        elif cmd_principal == "exit":
            return "", "normal", False, True
        elif cmd_principal == "help":
            return self._cmd_help()
        elif cmd_principal == "scan":
            return self._cmd_scan()
        elif cmd_principal == "clean":
            return self._cmd_clean()
        else:
            return (
                f"[X] ERROR: Comando desconocido: '{cmd_principal}'. Escribe 'help' para ver los 2 comandos.\n",
                "error",
                False,
                False
            )

    def _cmd_help(self):
        menu = (
            "=================== COMANDOS DE MITIGACION ===================\n"
            "  help    - Muestra este menu de ayuda.\n"
            "  scan    - Analiza el sistema simulado para encontrar el virus.\n"
            "  clean   - Elimina el virus y restaura el sistema (¡Victoria!).\n"
            "  clear   - Limpia el historial de la pantalla.\n"
            "  exit    - Abandona la simulacion.\n"
            "=============================================================="
        )
        return menu + "\n", "info", False, False

    def _cmd_scan(self):
        self.estado.scan_realizado = True
        return (
            "[OK] Analisis completo finalizado.\n"
            "[!] Amenaza localizada en el sistema.\n"
            "[!] Escribe 'clean' para erradicarla por completo y salvar el sistema.\n",
            "advertencia",
            False,
            False
        )

    def _cmd_clean(self):
        self.estado.salud_virus = 0.0
        self.estado.puntuacion += 1500
        
        self.estado.juego_activo = False
        self.estado.resultado_final = "VICTORIA"
        return (
            "[OK] Ejecutando protocolo de eliminacion...\n"
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
