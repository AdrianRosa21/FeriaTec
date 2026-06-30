import os
import json
import random
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from core.ranking_client import RankingClient

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def load_config():
    ruta_config = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
    try:
        with open(ruta_config, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "ranking_api_url": "http://localhost:3000/api/scores",
            "ranking_api_key": "feriatec-secret-key-2026"
        }

class AppFacil(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cyber Rescue - Modo Fácil")
        self.geometry("450x350")
        self.resizable(False, False)
        
        self.config = load_config()
        self.ranking_client = RankingClient(
            api_url=self.config.get("ranking_api_url", "http://localhost:3000/api/scores"),
            api_key=self.config.get("ranking_api_key", "feriatec-secret-key-2026")
        )
        
        self.grid_columnconfigure(0, weight=1)
        
        lbl_titulo = ctk.CTkLabel(
            self,
            text="CYBER RESCUE SIMULADOR",
            font=("Consolas", 18, "bold"),
            text_color="#10b981"
        )
        lbl_titulo.pack(pady=(20, 10))
        
        lbl_info = ctk.CTkLabel(
            self,
            text="¡Virus detectado!\nIngresa tus datos para eliminarlo y obtener tu certificado.",
            font=("Consolas", 12),
            text_color="#f87171"
        )
        lbl_info.pack(pady=(0, 20))
        
        self.entry_alias = ctk.CTkEntry(self, width=300, font=("Consolas", 12), placeholder_text="Tu Alias / Nombre")
        self.entry_alias.pack(pady=(5, 5))
        self.entry_alias.insert(0, f"Jugador_{random.randint(100, 999)}")
        
        self.entry_pass = ctk.CTkEntry(self, width=300, show="*", font=("Consolas", 12), placeholder_text="Contraseña (Mínimo 4 caracteres)")
        self.entry_pass.pack(pady=(5, 20))
        
        btn_scan = ctk.CTkButton(
            self,
            text="1. ANALIZAR SISTEMA",
            font=("Consolas", 12, "bold"),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            command=self.analizar
        )
        btn_scan.pack(pady=(5, 5))
        
        btn_clean = ctk.CTkButton(
            self,
            text="2. ELIMINAR VIRUS",
            font=("Consolas", 12, "bold"),
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self.eliminar
        )
        btn_clean.pack(pady=(5, 10))

    def analizar(self):
        messagebox.showwarning("Análisis", "¡Se ha detectado 1 amenaza en el sistema!\nUsa el botón 'Eliminar Virus' para ganar.")

    def eliminar(self):
        alias = self.entry_alias.get().strip()
        password = self.entry_pass.get().strip()
        
        if len(alias) < 2:
            messagebox.showerror("Error", "El alias debe tener al menos 2 caracteres.")
            return
        if len(password) < 4:
            messagebox.showerror("Error", "La contraseña debe tener al menos 4 caracteres.")
            return
            
        # Usamos el cliente ya configurado del proyecto original
        self.ranking_client.enviar_puntuacion_async(
            nombre=alias,
            puntuacion=2000,
            tiempo_restante=200,
            resultado="VICTORIA",
            password=password,
            callback=self.respuesta_ranking
        )
        
    def respuesta_ranking(self, exito, msj):
        if exito:
            self.after(0, lambda: messagebox.showinfo(
                "¡VICTORIA!", 
                "¡Virus eliminado con éxito!\nTu puntuación se ha guardado en el servidor.\nYa puedes pedir tu certificado."
            ))
        else:
            self.after(0, lambda: messagebox.showerror(
                "Error de Conexión", 
                f"Virus eliminado, pero no se pudo guardar la puntuación:\n{msj}\n¿Está encendido el servidor en el puerto 3000?"
            ))

if __name__ == "__main__":
    app = AppFacil()
    app.mainloop()
