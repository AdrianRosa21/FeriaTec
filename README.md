# 🖥️ Cyber Rescue & Live Ranking System

¡Bienvenido a **Cyber Rescue**! Una experiencia educativa interactiva diseñada para ferias tecnológicas y eventos de aprendizaje. Este proyecto combina una **simulación interactiva de consola de ciberseguridad** (Python/CustomTkinter) con un **monitor en vivo de clasificación y emisión de certificados** (Next.js/Firebase).

---

## 🎨 Arquitectura del Proyecto

El sistema está dividido en dos partes principales:

1. **Juego de Simulación (Escritorio):** Un videojuego simulado en Python donde los estudiantes actúan como analistas de ciberseguridad, mitigando un malware activo mediante comandos reales de consola.
2. **Dashboard de Clasificación (Web):** Una aplicación en Next.js conectada a Firebase Firestore que muestra las puntuaciones en tiempo real y permite emitir certificados oficiales a los ganadores de la feria.

---

## 🎮 1. Simulador Cyber Rescue (Juego de Escritorio)

La simulación simula un sistema comprometido por un malware (`virus.exe.fake`). El estudiante debe contener la amenaza interactuando con una terminal simulada.

### 🚀 Cómo Iniciar el Juego (Rápido)
Simplemente haz doble clic sobre el archivo ejecutable de Windows:
👉 **`ejecutar.bat`** (ubicado en la raíz del proyecto).

> [!NOTE]
> Este archivo `.bat` se encargará de verificar que tengas Python instalado, instalará las dependencias necesarias (`customtkinter` y `Pillow`) de forma automática, e iniciará el juego.

### 🛠️ Flujo de Comandos de Mitigación en el Juego
Una vez dentro del simulador, el estudiante debe seguir el protocolo de respuesta ante incidentes:
1. `scan` - Escanea el sandbox simulado y localiza el ejecutable de la amenaza.
2. `inspect virus` - Examina los detalles del malware (resta 10% de salud al virus).
3. `kill virus` - Detiene temporalmente el proceso del virus (resta 20% de salud).
4. `quarantine virus` - Mueve la amenaza a la carpeta segura de aislamiento (resta 25% de salud).
5. `delete virus` - Elimina permanentemente el archivo de la cuarentena (resta 20% de salud).
6. `repair system` - Repara el sector de restauración y logs del sistema (lleva la salud al 0%).
7. `restore` - Recupera la configuración limpia y original de fábrica (**¡Victoria!**).

---

## 📊 2. Monitor de Ranking & Certificados (Sistema Web)

Permite visualizar en tiempo real quién tiene la mayor puntuación en la feria técnica y permite descargar diplomas digitales.

### 🚀 Cómo Iniciar el Servidor Web Localmente
1. Abre tu terminal (PowerShell o CMD) y ve al directorio `ranking-system`:
   ```bash
   cd ranking-system
   ```
2. Instala las dependencias de Node.js:
   ```bash
   npm install
   ```
3. Inicia el servidor de desarrollo:
   ```bash
   npm run dev
   ```
4. Abre [http://localhost:3000](http://localhost:3000) en tu navegador preferido.

### 🎓 Descarga de Certificados Seguros
Cada vez que un estudiante completa con éxito la simulación, su puntaje se sincroniza al instante con el servidor.
* En el ranking web, aparecerá un botón de **CERTIFICADO** junto a su alias.
* Al hacer clic, el sistema le solicitará la **contraseña** que él mismo configuró al inicio de la simulación.
* Al desbloquearlo, se mostrará el diploma digital oficial listo para ser guardado como PDF o impreso (`Ctrl + P`).

---

## 🛠️ Tecnologías Utilizadas

* **Juego:** Python 3, CustomTkinter (UI moderna oscura), Pillow (Procesamiento de imágenes).
* **Frontend Web:** Next.js (App Router), React, Vanilla CSS (Estilos ciberpunk neón).
* **Base de Datos & Hosting:** Firebase Firestore (Almacenamiento de clasificación en tiempo real) y Vercel (Producción).

---
*Desarrollado para la Feria Técnica — Estudiantes de Desarrollo de Software.*
