import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import requests # type: ignore
import threading
import os

# ---------------- Diccionarios de descargas ----------------
descargas_programas = {
    "Adobe Photoshop CS6 Portable": "https://archive.org/download/adobe-photoshop-cs-6-portable/Adobe%20Photoshop%20CS6%20Portable.zip",
    "Lunar Magic": "https://dl.smwcentral.net/38972/lm351.zip",
    "DIE win64 Portable 3.11": "https://archive.org/download/die-win-64-portable-3.11/DIE%20win64%20Portable%203.11.zip",
    "JD Eclipse": "https://github.com/java-decompiler/jd-eclipse/releases/download/v2.0.0/jd-eclipse-2.0.0.zip",
}

descargas_wiiupc = {
    "UWUVCI AIO": "https://archive.org/download/uwuvci-aio/UWUVCI%20AIO.zip",
}

# ---------------- Función para descargar archivos ----------------
def descargar_archivo(url, nombre_archivo):
    def tarea():
        carpeta_destino = filedialog.askdirectory(title="Selecciona la carpeta para guardar el archivo")
        if not carpeta_destino:
            messagebox.showwarning("Cancelado", "No se seleccionó una carpeta.")
            return

        ruta_completa = os.path.join(carpeta_destino, nombre_archivo)

        # Comprobar si ya existe
        if os.path.exists(ruta_completa):
            respuesta = messagebox.askyesno("Archivo existente",
                                           f"El archivo '{nombre_archivo}' ya existe.\n¿Quieres reemplazarlo?")
            if not respuesta:
                return

        try:
            respuesta = requests.get(url, stream=True)
            respuesta.raise_for_status()

            total_size = int(respuesta.headers.get("content-length", 0))
            progress["maximum"] = total_size

            with open(ruta_completa, "wb") as f:
                downloaded = 0
                for chunk in respuesta.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        progress["value"] = downloaded
                        ventana.update_idletasks()

            messagebox.showinfo("Éxito", f"Archivo descargado correctamente en:\n{ruta_completa}")
            progress["value"] = 0
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"No se pudo descargar el archivo:\n{e}")

    threading.Thread(target=tarea).start()

# ---------------- Función para cambiar de página ----------------
def mostrar_pagina(pagina):
    for frame in (pagina_inicio, pagina_programas, pagina_wiiupc):
        frame.pack_forget()
    pagina.pack(fill="both", expand=True)

# ---------------- Ventana principal ----------------
ventana = tk.Tk()
ventana.title("Lorenzo's Downloader")
ventana.geometry("500x500")

# Barra de progreso
progress = ttk.Progressbar(ventana, length=400, mode="determinate")
progress.pack(pady=5)

# ---------------- Página de Inicio ----------------
pagina_inicio = tk.Frame(ventana)
tk.Label(pagina_inicio, text="Welcome to Lorenzo's Downloader", font=("Arial", 18)).pack(pady=20)

tk.Button(pagina_inicio, text="Programs", font=("Arial", 14),
          command=lambda: mostrar_pagina(pagina_programas), bg="lightgreen").pack(pady=10)

tk.Button(pagina_inicio, text="Exit", font=("Arial", 14),
          command=ventana.destroy, bg="tomato").pack(pady=10)

# ---------------- Página Programas ----------------
pagina_programas = tk.Frame(ventana)
tk.Label(pagina_programas, text="Descargar Programas", font=("Arial", 18)).pack(pady=10)

# Botón para ir a Wii U (PC)
tk.Button(pagina_programas, text="Wii U (PC)", font=("Arial", 14),
          command=lambda: mostrar_pagina(pagina_wiiupc), bg="lightgreen").pack(pady=10)

# Botones de descarga de programas
for nombre, url in descargas_programas.items():
    extension = os.path.splitext(url)[1]
    tk.Button(pagina_programas, text=nombre, font=("Arial", 12),
              command=lambda url=url, nombre=nombre, ext=extension: descargar_archivo(url, nombre + ext),
              bg="lightblue").pack(pady=5)

tk.Button(pagina_programas, text="Go Back", font=("Arial", 12),
          command=lambda: mostrar_pagina(pagina_inicio), bg="orange").pack(pady=20)

# ---------------- Página Wii U (PC) ----------------
pagina_wiiupc = tk.Frame(ventana)
tk.Label(pagina_wiiupc, text="Descargar Programas de Wii U (PC)", font=("Arial", 18)).pack(pady=10)

for nombre, url in descargas_wiiupc.items():
    extension = os.path.splitext(url)[1]
    tk.Button(pagina_wiiupc, text=nombre, font=("Arial", 12),
              command=lambda url=url, nombre=nombre, ext=extension: descargar_archivo(url, nombre + ext),
              bg="lightblue").pack(pady=5)

tk.Button(pagina_wiiupc, text="Go Back", font=("Arial", 12),
          command=lambda: mostrar_pagina(pagina_programas), bg="orange").pack(pady=20)

# ---------------- Iniciar aplicación ----------------
mostrar_pagina(pagina_inicio)
ventana.mainloop()
