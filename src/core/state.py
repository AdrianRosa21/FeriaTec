# -*- coding: utf-8 -*-

class EstadoSimulacion:
    def __init__(self):
        self.reiniciar_estado()

    def reiniciar_estado(self):
        # Variables de juego principales
        self.salud_virus = 1.0  # 1.0 = 100%
        self.puntuacion = 1000
        self.tiempo_restante = 180  # 3 minutos en segundos
        self.juego_activo = True
        self.resultado_final = None  # Puede ser "VICTORIA" o "DERROTA"

        # Banderas de secuencia lógica de comandos
        self.scan_realizado = False
        self.logs_vistos = False
        self.procesos_vistos = False
        self.virus_inspeccionado = False
        self.temporal_limpiado = False
        self.proceso_muerto = False
        self.virus_en_cuarentena = False
        self.virus_eliminado = False
        self.sistema_reparado = False

    def obtener_porcentaje_salud(self):
        return int(self.salud_virus * 100)
