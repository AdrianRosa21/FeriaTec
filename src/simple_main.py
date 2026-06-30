import os
import json

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

def main():
    print("==================================================")
    print("      CYBER RESCUE - MODO FACIL (SOLO CONSOLA)    ")
    print("==================================================")
    
    config = load_config()
    api_url = config.get("ranking_api_url", "http://localhost:3000/api/scores")
    api_key = config.get("ranking_api_key", "feriatec-secret-key-2026")
    
    print("\n[!] Alerta: Virus detectado en el sistema.")
    print("Para obtener tu certificado, debes erradicar el virus.\n")
    
    nombre = input("Ingresa tu alias de jugador: ")
    password = input("Ingresa una contrasena (min 4 caracteres): ")
    
    while True:
        print("\nComandos disponibles:")
        print("  1 - Analizar sistema (scan)")
        print("  2 - Eliminar virus (clean)")
        print("  3 - Salir (exit)")
        
        opcion = input("\nSelecciona un comando (1-3): ").strip()
        
        if opcion == "1" or opcion.lower() == "scan":
            print("\nAnalizando... [||||||||||||||||||||] 100%")
            print("Resultado: Archivos infectados = 1. El virus sigue presente.")
        elif opcion == "2" or opcion.lower() == "clean":
            print("\nEjecutando protocolo de eliminacion...")
            print("[OK] Virus eliminado con exito. ¡Has salvado el sistema!")
            print("\nSincronizando puntuacion con el servidor de ranking...")
            
            import urllib.request
            import urllib.error
            payload = {
                "player_name": nombre,
                "score": 1500,
                "time_left": 150,
                "status": "VICTORIA",
                "password": password
            }
            try:
                req = urllib.request.Request(api_url, data=json.dumps(payload).encode("utf-8"), method="POST")
                req.add_header("Content-Type", "application/json")
                req.add_header("Authorization", f"Bearer {api_key}")
                with urllib.request.urlopen(req, timeout=5) as response:
                    print("[OK] ¡Puntuacion registrada correctamente!")
                    print("[!] Pide al encargado que te imprima/muestre tu certificado de VICTORIA.")
            except Exception as e:
                print(f"[X] ERROR de conexion con ranking: {str(e)}")
                print("[!] Asegurate de que el servidor Next.js este corriendo (npm run dev).")
            
            print("\nPresiona ENTER para salir...")
            input()
            break
        elif opcion == "3" or opcion.lower() == "exit":
            print("Saliendo de la simulacion...")
            break
        else:
            print("Comando no reconocido. Usa 1, 2 o 3.")

if __name__ == "__main__":
    main()
