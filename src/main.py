# -*- coding: utf-8 -*-
import os
import json
import random
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image

from utils.ascii_art import BANNER
from core.state import EstadoSimulacion
from core.filesystem import SandboxFilesystem
from core.interpreter import InterpreteComandos
from core.ranking_client import RankingClient

# Configuración del tema y apariencia de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AlertaFalsaWindows(ctk.CTkToplevel):
    def __init__(self, master, mensaje):
        super().__init__(master)
        self.title("Critical Threat Warning")
        self.geometry("460x170")
        self.resizable(False, False)
        self.attributes("-topmost", True)  # Mantener al frente
        
        # Sonar campana del sistema
        self.bell()
        
        # Configuración de cuadrícula
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        
        # Icono de advertencia en ASCII
        self.lbl_icono = ctk.CTkLabel(
            self,
            text=" [!] ",
            text_color="#ef4444",
            font=("Consolas", 32, "bold")
        )
        self.lbl_icono.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Mensaje de advertencia
        self.lbl_msg = ctk.CTkLabel(
            self,
            text=f"AMENAZA DETECTADA:\n{mensaje}\n\n(Simulacion Educativa Autorizada)",
            text_color="#ef4444",
            font=("Consolas", 12, "bold"),
            justify="left",
            wraplength=320
        )
        self.lbl_msg.grid(row=0, column=1, padx=10, pady=20, sticky="w")
        
        # Botón para cerrar alerta
        self.btn_aceptar = ctk.CTkButton(
            self,
            text="ACEPTAR",
            font=("Consolas", 11, "bold"),
            fg_color="#ef4444",
            hover_color="#b91c1c",
            text_color="#ffffff",
            width=100,
            corner_radius=0,
            command=self.cerrar_alerta
        )
        self.btn_aceptar.grid(row=1, column=0, columnspan=2, pady=(0, 15))
        
        self.focus()
        self.grab_set()  # Modal: fuerza la interacción con esta ventana antes de seguir

    def cerrar_alerta(self):
        self.grab_release()
        self.destroy()


class VentanaVidaVirus(ctk.CTkToplevel):
    def __init__(self, master, img_corazon):
        super().__init__(master)
        self.master_app = master
        self.title("Virus Health Monitor")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        
        # Impedir el cierre manual individual en la feria técnica
        self.protocol("WM_DELETE_WINDOW", lambda: None)

        # Ubicar en la esquina superior derecha de la pantalla
        ancho_pantalla = self.winfo_screenwidth()
        pos_x = ancho_pantalla - 320
        self.geometry(f"300x130+{pos_x}+40")

        # Componentes de interfaz
        self.crear_componentes(img_corazon)

    def crear_componentes(self, img_corazon):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.panel = ctk.CTkFrame(self, fg_color="#0f172a", border_color="#ef4444", border_width=2, corner_radius=0)
        self.panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.panel.grid_columnconfigure(0, weight=0)
        self.panel.grid_columnconfigure(1, weight=1)

        # Corazón de Isaac (se remueve sticky="center" para evitar la excepcion en Tkinter)
        if img_corazon:
            self.lbl_corazon = ctk.CTkLabel(self.panel, image=img_corazon, text="")
            self.lbl_corazon.grid(row=0, column=0, rowspan=3, padx=15, pady=10)
        else:
            self.lbl_corazon = ctk.CTkLabel(self.panel, text="<3", font=("Consolas", 24, "bold"), text_color="#ef4444")
            self.lbl_corazon.grid(row=0, column=0, rowspan=3, padx=15, pady=10)

        # Salud
        self.lbl_salud = ctk.CTkLabel(
            self.panel,
            text="SALUD VIRUS: 100%",
            text_color="#ef4444",
            font=("Consolas", 14, "bold")
        )
        self.lbl_salud.grid(row=0, column=1, sticky="w", pady=(10, 0))

        self.bar_salud = ctk.CTkProgressBar(
            self.panel,
            progress_color="#ef4444",
            bg_color="#334155",
            width=180,
            height=10
        )
        self.bar_salud.set(1.0)
        self.bar_salud.grid(row=1, column=1, sticky="w", pady=(2, 5))

        # Tiempo restante (abajo de la salud)
        self.lbl_tiempo = ctk.CTkLabel(
            self.panel,
            text="TIEMPO: 03:00",
            text_color="#f59e0b",
            font=("Consolas", 12, "bold")
        )
        self.lbl_tiempo.grid(row=2, column=1, sticky="w", pady=(0, 10))

    def actualizar(self, salud_virus, salud_pct, tiempo_texto, color_tiempo):
        self.bar_salud.set(salud_virus)
        self.lbl_salud.configure(text=f"SALUD VIRUS: {salud_pct}%")
        self.lbl_tiempo.configure(text=tiempo_texto, text_color=color_tiempo)


class VentanaAmenazaVirus(ctk.CTkToplevel):
    def __init__(self, master, img_calavera):
        super().__init__(master)
        self.master_app = master
        self.title("Virus Threat Monitor")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        
        # Impedir el cierre manual individual en la feria técnica
        self.protocol("WM_DELETE_WINDOW", lambda: None)

        # Ubicar pegado al borde izquierdo de la pantalla
        alto_pantalla = self.winfo_screenheight()
        pos_y = (alto_pantalla // 2) - 225
        self.geometry(f"280x430+20+{pos_y}")

        # Componentes de interfaz
        self.crear_componentes(img_calavera)

    def crear_componentes(self, img_calavera):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.panel = ctk.CTkFrame(self, fg_color="#050505", border_color="#ef4444", border_width=2, corner_radius=0)
        self.panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Calavera cyber
        if img_calavera:
            # Reajustar tamaño para ventana flotante
            self.lbl_calavera = ctk.CTkLabel(self.panel, image=img_calavera, text="")
            self.lbl_calavera.pack(pady=(20, 10))
        else:
            self.lbl_calavera = ctk.CTkLabel(
                self.panel,
                text="  [XXXXX]\n [X X X]\n  [XXX]\n   X X",
                font=("Consolas", 16, "bold"),
                text_color="#ef4444"
            )
            self.lbl_calavera.pack(pady=(20, 10))

        self.lbl_titulo = ctk.CTkLabel(
            self.panel,
            text="VIRUS MONITOREADO",
            text_color="#ef4444",
            font=("Consolas", 12, "bold")
        )
        self.lbl_titulo.pack(pady=5)

        # Texto con efectos
        self.lbl_msg = ctk.CTkLabel(
            self.panel,
            text="SISTEMA BAJO ATAQUE",
            text_color="#ef4444",
            font=("Consolas", 13, "bold"),
            wraplength=240,
            justify="center"
        )
        self.lbl_msg.pack(pady=(20, 10), fill="x", padx=10)

    def actualizar_mensaje(self, mensaje, color):
        self.lbl_msg.configure(text=mensaje, text_color=color)


class VentanaRegistroJugador(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Registro de Estudiante")
        self.geometry("380x260")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.grab_set()

        self.nombre = ""
        self.password = ""
        self.confirmado = False

        self.grid_columnconfigure(0, weight=1)
        
        lbl_titulo = ctk.CTkLabel(
            self,
            text="REGISTRO DE EXPERIENCIA CYBER RESCUE",
            font=("Consolas", 13, "bold"),
            text_color="#10b981"
        )
        lbl_titulo.pack(pady=(20, 10))

        # Field 1: Alias
        lbl_alias = ctk.CTkLabel(self, text="Alias / Nombre del Estudiante:", font=("Consolas", 11))
        lbl_alias.pack(anchor="w", padx=40)
        self.entry_alias = ctk.CTkEntry(self, width=300, font=("Consolas", 12))
        self.entry_alias.pack(pady=(2, 10))
        self.entry_alias.insert(0, f"Jugador_{random.randint(100, 999)}")

        # Field 2: Password
        lbl_pass = ctk.CTkLabel(self, text="Contraseña del Certificado (Mínimo 4 caracteres):", font=("Consolas", 11))
        lbl_pass.pack(anchor="w", padx=40)
        self.entry_pass = ctk.CTkEntry(self, width=300, show="*", font=("Consolas", 12))
        self.entry_pass.pack(pady=(2, 15))

        btn_confirmar = ctk.CTkButton(
            self,
            text="INICIAR SIMULACIÓN",
            font=("Consolas", 12, "bold"),
            fg_color="#10b981",
            text_color="#000000",
            hover_color="#059669",
            command=self.confirmar
        )
        btn_confirmar.pack(pady=5)

        self.bind("<Return>", lambda e: self.confirmar())
        self.focus()
        self.master.wait_window(self)

    def confirmar(self):
        alias = self.entry_alias.get().strip()
        pwd = self.entry_pass.get().strip()

        if not alias:
            messagebox.showwarning("Registro Inválido", "Por favor ingresa un nombre o alias.")
            return
        if len(pwd) < 4:
            messagebox.showwarning("Registro Inválido", "La contraseña debe tener al menos 4 caracteres.")
            return

        self.nombre = alias[:20]
        self.password = pwd
        self.confirmado = True
        self.grab_release()
        self.destroy()


class AplicacionCyberRescue(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Cargar configuración desde config.json
        self.configuracion = self.cargar_configuracion()

        # Configuración de la ventana principal de la terminal
        self.title(self.configuracion.get("titulo_consola", "CYBER RESCUE WINDOWS"))
        self.geometry("820x600")
        self.resizable(False, False)

        # Centrar la ventana principal
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()
        pos_x = (ancho_pantalla // 2) - 410
        pos_y = (alto_pantalla // 2) - 300
        self.geometry(f"820x600+{pos_x}+{pos_y}")

        # Inicializar subsistemas del core
        self.estado = EstadoSimulacion()
        self.filesystem = SandboxFilesystem()
        self.interprete = InterpreteComandos(self.estado, self.filesystem)

        # Inicializar cliente de ranking
        self.ranking_client = RankingClient(
            self.configuracion.get("ranking_api_url"),
            self.configuracion.get("ranking_api_key")
        )
        
        self.nombre_jugador = "Jugador"
        self.pedir_nombre_jugador()

        # Cargar recursos de imagen
        self.cargar_imagenes()

        # Crear ventanas flotantes independientes
        self.ventana_vida = VentanaVidaVirus(self, self.img_corazon)
        self.ventana_amenaza = VentanaAmenazaVirus(self, self.img_calavera)

        # Crear estructura de la terminal principal
        self.crear_componentes()

        # Iniciar bucles del juego
        self.actualizar_temporizador()
        self.lanzar_mensaje_virus_aleatorio()
        self.animar_alerta_virus()

        # Cargar estado inicial en pantalla
        self.escribir_bienvenida()

    def pedir_nombre_jugador(self):
        self.password_jugador = ""
        try:
            # Abrir ventana de registro personalizada
            reg_win = VentanaRegistroJugador(self)
            if reg_win.confirmado:
                self.nombre_jugador = reg_win.nombre
                self.password_jugador = reg_win.password
            else:
                self.nombre_jugador = "Anonimo_" + str(random.randint(100, 999))
                self.password_jugador = "12345"
        except Exception as e:
            print("Error en registro:", e)
            self.nombre_jugador = "Jugador"
            self.password_jugador = "12345"

    def cargar_configuracion(self):
        ruta_config = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
        try:
            with open(ruta_config, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {
                "titulo_consola": "CYBER RESCUE WINDOWS - SIMULACION EDUCATIVA",
                "virus_nombre": "virus",
                "mensajes": {
                    "bienvenida": "[OK] Sistema de archivos simulado inicializado en ./simulation_data/\n[WARNING] virus detectado en memoria.\nEscribe 'help' para ver los comandos de mitigacion.",
                    "simulacion_educativa": "ATENCION: ESTO ES UNA SIMULACION EDUCATIVA. NO SE MODIFICARAN ARCHIVOS REALES DE TU EQUIPO.",
                    "ayuda": "Comandos: help, scan, status, logs, processes, inspect virus, kill virus, clean temp, quarantine virus, delete virus, repair system, restore, clear, exit"
                }
            }

    def cargar_imagenes(self):
        ruta_assets = os.path.join(os.path.dirname(__file__), "assets")
        self.img_corazon = None
        self.img_calavera = None

        try:
            ruta_corazon = os.path.join(ruta_assets, "corazon.png")
            if os.path.exists(ruta_corazon):
                img_p = Image.open(ruta_corazon)
                self.img_corazon = ctk.CTkImage(light_image=img_p, dark_image=img_p, size=(30, 30))

            ruta_calavera = os.path.join(ruta_assets, "calavera.png")
            if os.path.exists(ruta_calavera):
                img_c = Image.open(ruta_calavera)
                # Ajustar calavera a tamaño de widget en ventana flotante
                self.img_calavera = ctk.CTkImage(light_image=img_c, dark_image=img_c, size=(110, 110))
        except Exception as e:
            print(f"[!] Error al cargar imagenes de assets: {e}")

    def crear_componentes(self):
        # Grid para la ventana principal
        self.grid_rowconfigure(0, weight=0)  # Cabecera
        self.grid_rowconfigure(1, weight=0)  # Stats de terminal (Puntuación)
        self.grid_rowconfigure(2, weight=1)  # Terminal
        self.grid_rowconfigure(3, weight=0)  # Entrada
        self.grid_columnconfigure(0, weight=1)

        # 1. Cabecera
        self.cabecera_frame = ctk.CTkFrame(self, fg_color="#f59e0b", height=35, corner_radius=0)
        self.cabecera_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.cabecera_frame.grid_columnconfigure(0, weight=1)
        self.cabecera_frame.grid_columnconfigure(1, weight=0)

        self.lbl_cabecera = ctk.CTkLabel(
            self.cabecera_frame,
            text=f"[!] {self.configuracion['mensajes']['simulacion_educativa'].upper()} [!]",
            text_color="#000000",
            font=("Consolas", 12, "bold")
        )
        self.lbl_cabecera.grid(row=0, column=0, padx=20, pady=4, sticky="w")

        self.btn_reset_secreto = ctk.CTkButton(
            self.cabecera_frame,
            text="[ REINICIAR ]",
            font=("Consolas", 10, "bold"),
            fg_color="#000000",
            hover_color="#1e293b",
            text_color="#f59e0b",
            corner_radius=4,
            width=100,
            command=self.confirmar_reinicio
        )
        self.btn_reset_secreto.grid(row=0, column=1, padx=10, pady=4, sticky="e")

        # 2. Panel superior de Stats (Solo Puntuación para dejar limpia la terminal)
        self.panel_stats = ctk.CTkFrame(self, fg_color="#0f172a", height=50, corner_radius=0)
        self.panel_stats.grid(row=1, column=0, sticky="ew", padx=0, pady=2)
        self.panel_stats.grid_columnconfigure(0, weight=1)
        self.panel_stats.grid_columnconfigure(1, weight=1)

        self.lbl_titulo_juego = ctk.CTkLabel(
            self.panel_stats,
            text=f"JUGADOR: {self.nombre_jugador.upper()} | CORE INTERFACE v1.0",
            text_color="#10b981",
            font=("Consolas", 12, "bold")
        )
        self.lbl_titulo_juego.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.lbl_puntos = ctk.CTkLabel(
            self.panel_stats,
            text="PUNTUACION: 1000 PTS",
            text_color="#10b981",
            font=("Consolas", 14, "bold")
        )
        self.lbl_puntos.grid(row=0, column=1, padx=20, pady=10, sticky="e")

        # 3. Terminal interactiva (Ocupa todo el centro)
        self.txt_terminal = ctk.CTkTextbox(
            self,
            font=("Consolas", 13),
            text_color="#10b981",
            fg_color="#000000",
            border_color="#1e293b",
            border_width=2,
            corner_radius=0
        )
        self.txt_terminal.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        
        # Tags de la terminal
        self.txt_terminal.tag_config("normal", foreground="#10b981")
        self.txt_terminal.tag_config("error", foreground="#ef4444")
        self.txt_terminal.tag_config("advertencia", foreground="#f59e0b")
        self.txt_terminal.tag_config("info", foreground="#60a5fa")
        self.txt_terminal.tag_config("virus", foreground="#ef4444")
        self.txt_terminal.configure(state="disabled")

        # 4. Entrada de comandos
        self.frame_entrada = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_entrada.grid(row=3, column=0, sticky="ew", padx=10, pady=(5, 15))
        self.frame_entrada.grid_columnconfigure(0, weight=1)
        self.frame_entrada.grid_columnconfigure(1, weight=0)

        self.entry_comando = ctk.CTkEntry(
            self.frame_entrada,
            font=("Consolas", 14),
            text_color="#10b981",
            fg_color="#000000",
            border_color="#1e293b",
            border_width=2,
            corner_radius=0,
            placeholder_text="Escribe un comando de mitigación..."
        )
        self.entry_comando.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.entry_comando.bind("<Return>", self.procesar_comando_event)

        self.btn_ejecutar = ctk.CTkButton(
            self.frame_entrada,
            text="EJECUTAR",
            font=("Consolas", 13, "bold"),
            fg_color="#1e293b",
            hover_color="#334155",
            text_color="#10b981",
            border_color="#10b981",
            border_width=1,
            corner_radius=0,
            width=120,
            command=self.procesar_comando
        )
        self.btn_ejecutar.grid(row=0, column=1, sticky="ns")

    def escribir_en_terminal(self, texto, tag="normal"):
        self.txt_terminal.configure(state="normal")
        self.txt_terminal.insert("end", texto, tag)
        self.txt_terminal.see("end")
        self.txt_terminal.configure(state="disabled")

    def escribir_bienvenida(self):
        self.txt_terminal.configure(state="normal")
        self.txt_terminal.delete("1.0", "end")
        self.txt_terminal.configure(state="disabled")
        
        self.escribir_en_terminal(BANNER, "info")
        self.escribir_en_terminal(self.configuracion["mensajes"]["bienvenida"] + "\n", "advertencia")
        self.escribir_en_terminal("\nC:\\RescueSimulation> ", "normal")

    def actualizar_temporizador(self):
        if not self.estado.juego_activo:
            return

        minutos = self.estado.tiempo_restante // 60
        segundos = self.estado.tiempo_restante % 60
        tiempo_texto = f"TIEMPO: {minutos:02d}:{segundos:02d}"

        # Determinar colores del tiempo
        if self.estado.tiempo_restante <= 60:
            color_tiempo = "#ef4444"  # Rojo
        else:
            color_tiempo = "#f59e0b"  # Amarillo

        # Actualizar en la ventana flotante de vida
        if self.ventana_vida.winfo_exists():
            self.ventana_vida.actualizar(
                self.estado.salud_virus,
                self.estado.obtener_porcentaje_salud(),
                tiempo_texto,
                color_tiempo
            )

        if self.estado.tiempo_restante <= 0:
            self.estado.juego_activo = False
            self.estado.resultado_final = "DERROTA"
            self.finalizar_juego(victoria=False)
            return

        self.estado.tiempo_restante -= 1
        self.after(1000, self.actualizar_temporizador)

    def lanzar_mensaje_virus_aleatorio(self):
        if not self.estado.juego_activo:
            return

        if not self.estado.virus_eliminado:
            # Lista de frases de amenaza del virus en mayúsculas agresivas y ondas de "VAS A PERDER TUS ARCHIVOS"
            frases_agresivas = [
                "¡VAS A PERDER TODOS TUS ARCHIVOS!",
                "¡EL SISTEMA YA ES MÍO, INTRUSO!",
                "¡NO PODRÁS SALVAR TU INFORMACIÓN!",
                "¡CADA INTENTO ES INÚTIL, RÍNDETE!",
                "¡BORRANDO REGISTROS SIMULADOS!",
                "¡EL RELOJ SIGUE CORRIENDO, PIERDES TIEMPO!",
                "¡BLOQUEANDO ACCESO INTERNO!"
            ]
            msg = random.choice(frases_agresivas)
            
            # 1. Actualizar el panel lateral flotante de la calavera
            if self.ventana_amenaza.winfo_exists():
                self.ventana_amenaza.actualizar_mensaje(msg, "#ef4444")
            
            # 2. Escribir en la terminal el mensaje
            self.escribir_en_terminal(f"\n[!] ALERTA DEL VIRUS: {msg}\n", "virus")
            self.escribir_en_terminal("C:\\RescueSimulation> ", "normal")

            # 3. Lanzar mini modal/alerta emergente de error de Windows simulada
            self.lanzar_alerta_falsa_emergente(msg)

        # Ocurre exactamente cada 20 segundos
        self.after(20000, self.lanzar_mensaje_virus_aleatorio)

    def lanzar_alerta_falsa_emergente(self, mensaje):
        # Crear alerta emergente simulando error del sistema
        AlertaFalsaWindows(self, mensaje)

    def animar_alerta_virus(self):
        if not self.winfo_exists():
            return

        if not self.estado.juego_activo:
            return

        # Si el virus ya fue eliminado, reflejarlo en la calavera flotante
        if self.estado.virus_eliminado:
            if self.ventana_amenaza.winfo_exists():
                self.ventana_amenaza.actualizar_mensaje("SISTEMA SEGURO\nAMENAZA ERRADICADA", "#10b981")
            return

        # Parpadeo del texto en la ventana flotante de la calavera
        if self.ventana_amenaza.winfo_exists():
            color_actual = self.ventana_amenaza.lbl_msg.cget("text_color")
            nuevo_color = "#ef4444" if color_actual != "#ef4444" else "#475569"
            self.ventana_amenaza.actualizar_mensaje(self.ventana_amenaza.lbl_msg.cget("text"), nuevo_color)

        self.after(500, self.animar_alerta_virus)

    def procesar_comando_event(self, event):
        self.procesar_comando()

    def procesar_comando(self):
        if not self.estado.juego_activo:
            return

        comando = self.entry_comando.get().strip()
        if not comando:
            return

        self.entry_comando.delete(0, "end")
        self.escribir_en_terminal(f"{comando}\n", "normal")

        partes = comando.lower().split()
        cmd_principal = partes[0]

        if cmd_principal == "scan":
            self.ejecutar_escaneo_con_retardo()
        else:
            mensaje, tag, limpiar, salir = self.interprete.procesar(comando)

            if salir:
                self.destroy()
                return

            if limpiar:
                self.txt_terminal.configure(state="normal")
                self.txt_terminal.delete("1.0", "end")
                self.txt_terminal.configure(state="disabled")
            else:
                self.escribir_en_terminal(mensaje, tag)

            # Actualizar todos los widgets y ventanas secundarias
            self.actualizar_widgets()

            if not self.estado.juego_activo and self.estado.resultado_final == "VICTORIA":
                self.finalizar_juego(victoria=True)
            else:
                if not limpiar:
                    self.escribir_en_terminal("C:\\RescueSimulation> ", "normal")

    def ejecutar_escaneo_con_retardo(self):
        self.escribir_en_terminal("[!] Iniciando escaneo del sandbox simulado...\n", "advertencia")
        self.btn_ejecutar.configure(state="disabled")
        self.entry_comando.configure(state="disabled")

        def completar_escaneo():
            mensaje, tag, _, _ = self.interprete.procesar("scan")
            self.escribir_en_terminal(mensaje, tag)
            self.actualizar_widgets()
            
            self.btn_ejecutar.configure(state="normal")
            self.entry_comando.configure(state="normal")
            self.entry_comando.focus()
            self.escribir_en_terminal("C:\\RescueSimulation> ", "normal")

        self.after(1500, completar_escaneo)

    def actualizar_widgets(self):
        salud_pct = self.estado.obtener_porcentaje_salud()
        tiempo_texto = f"TIEMPO: {self.estado.tiempo_restante // 60:02d}:{self.estado.tiempo_restante % 60:02d}"
        color_tiempo = "#ef4444" if self.estado.tiempo_restante <= 60 else "#f59e0b"

        # 1. Actualizar ventana flotante de salud
        if self.ventana_vida.winfo_exists():
            self.ventana_vida.actualizar(self.estado.salud_virus, salud_pct, tiempo_texto, color_tiempo)

        # 2. Actualizar ventana flotante de la calavera si se elimino
        if self.estado.virus_eliminado:
            if self.ventana_amenaza.winfo_exists():
                self.ventana_amenaza.actualizar_mensaje("SISTEMA SEGURO\nAMENAZA ERRADICADA", "#10b981")

        # 3. Actualizar puntuación
        self.lbl_puntos.configure(text=f"PUNTUACION: {self.estado.puntuacion} PTS")

        # 4. Actualizar nombre de jugador
        self.lbl_titulo_juego.configure(text=f"JUGADOR: {self.nombre_jugador.upper()} | CORE INTERFACE v1.0")

    def finalizar_juego(self, victoria):
        self.estado.juego_activo = False
        self.btn_ejecutar.configure(state="disabled")
        self.entry_comando.configure(state="disabled")

        self.txt_terminal.configure(state="normal")
        self.txt_terminal.delete("1.0", "end")
        self.txt_terminal.configure(state="disabled")

        if victoria:
            banner_vic = (
                "==========================================================\n"
                "  __      _______ _____ _______ ____  _____  _____         \n"
                "  \\ \\    / /_   _/ ____|__   __/ __ \\|  __ \\|_   _|   /\\   \n"
                "   \\ \\  / /  | || |       | | | |  | | |__) | | |    /  \\  \n"
                "    \\ \\/ /   | || |       | | | |  | |  _  /  | |   / /\\ \\ \n"
                "     \\  /   _| || |____   | | | |__| | | \\ \\ _| |_ / ____ \\\n"
                "      \\/   |_____\\_____|  |_|  \\____/|_|  \\_\\_____/_/    \\_\\\n"
                "==========================================================\n"
            )
            self.escribir_en_terminal(banner_vic, "normal")
            self.escribir_en_terminal(
                f"[OK] ¡virus ha sido completamente erradicado!\n"
                f"[OK] El sistema simulado ha sido restaurado a su estado de fabrica.\n\n"
                f"  * Puntuacion final realizada: {self.estado.puntuacion} PTS\n"
                f"  * Tiempo sobrante: {self.estado.tiempo_restante // 60:02d}:{self.estado.tiempo_restante % 60:02d}\n\n"
                "[!] Pide al encargado de la feria que registre tu puntuacion.\n"
                "    Usa el boton 'REINICIAR' de la cabecera para otra partida.\n",
                "info"
            )
            if self.ventana_vida.winfo_exists():
                self.ventana_vida.actualizar(0.0, 0, "SISTEMA SEGURO", "#10b981")
            if self.ventana_amenaza.winfo_exists():
                self.ventana_amenaza.actualizar_mensaje("VICTORIA: SISTEMA SEGURO", "#10b981")
        else:
            banner_der = (
                "==========================================================\n"
                "   _____          __  __ ______    ______     ________ ____ \n"
                "  / ____|   /\\   |  \\/  |  ____|  / __ \\ \\   / /  ____|  _ \\\n"
                " | |  __   /  \\  | \\  / | |__    | |  | \\ \\_/ /| |__  | |_) |\n"
                " | | |_ | / /\\ \\ | |\\/| |  __|   | |  | |\\   / |  __| |  _ < \n"
                " | |__| |/ ____ \\| |  | | |____  | |__| | | |  | |____| |_) |\n"
                "  \\_____/_/    \\_\\_|  |_|______|  \\____/  |_|  |______|____/ \n"
                "==========================================================\n"
            )
            self.escribir_en_terminal(banner_der, "error")
            self.escribir_en_terminal(
                f"[X] SISTEMA COMPLETAMENTE COMPROMETIDO\n"
                f"[X] Se agoto el tiempo limite de contencion.\n"
                f"[X] virus ha cifrado la base de datos de restauracion virtual.\n\n"
                f"  * Puntuacion final: {self.estado.puntuacion} PTS\n\n"
                "[!] No te rindas. Intenta de nuevo presionando el boton 'REINICIAR' de la cabecera.\n",
                "advertencia"
            )
            if self.ventana_vida.winfo_exists():
                self.ventana_vida.actualizar(self.estado.salud_virus, self.estado.obtener_porcentaje_salud(), "SISTEMA CIFRADO", "#ef4444")
            if self.ventana_amenaza.winfo_exists():
                self.ventana_amenaza.actualizar_mensaje("SISTEMA BLOQUEADO: DETENIDO", "#ef4444")

        # Enviar puntuación al servidor de ranking de forma asíncrona
        self.escribir_en_terminal("\n[!] Sincronizando puntuacion con el servidor de ranking...\n", "info")
        
        def callback_ranking(exito, mensaje_error):
            def gui_callback():
                if exito:
                    self.escribir_en_terminal("[OK] Puntuacion registrada en el servidor con exito.\n", "info")
                else:
                    self.escribir_en_terminal(f"[X] ERROR de conexion con ranking: {mensaje_error}\n", "error")
                    self.escribir_en_terminal("[!] Pide al encargado que registre tu puntuacion manualmente.\n", "advertencia")
                self.escribir_en_terminal("\nC:\\RescueSimulation> ", "normal")
            
            self.after(0, gui_callback)

        self.ranking_client.enviar_puntuacion_async(
            self.nombre_jugador,
            self.estado.puntuacion,
            self.estado.tiempo_restante,
            "VICTORIA" if victoria else "DERROTA",
            self.password_jugador,
            callback_ranking
        )

    def confirmar_reinicio(self):
        respuesta = messagebox.askyesno(
            "Confirmar Reinicio",
            "¿Desea reiniciar la experiencia educativa y restaurar los archivos del sandbox?"
        )
        if respuesta:
            self.reiniciar_juego()

    def reiniciar_juego(self):
        # Pedir nombre de nuevo para la nueva partida
        self.pedir_nombre_jugador()
        
        # Restablecer estado lógico
        self.estado.reiniciar_estado()
        
        # Restablecer sandbox físico en simulación
        self.filesystem.reiniciar_sandbox()

        # Re-habilitar controles
        self.btn_ejecutar.configure(state="normal")
        self.entry_comando.configure(state="normal")
        self.entry_comando.delete(0, "end")
        self.entry_comando.focus()

        # Si se hubieran cerrado las ventanas flotantes, volver a abrirlas
        if not self.ventana_vida.winfo_exists():
            self.ventana_vida = VentanaVidaVirus(self, self.img_corazon)
        if not self.ventana_amenaza.winfo_exists():
            self.ventana_amenaza = VentanaAmenazaVirus(self, self.img_calavera)

        # Actualizar widgets
        self.actualizar_widgets()

        # Volver a escribir bienvenida
        self.escribir_bienvenida()

        # Reiniciar los bucles de eventos
        self.actualizar_temporizador()

if __name__ == "__main__":
    app = AplicacionCyberRescue()
    app.mainloop()
