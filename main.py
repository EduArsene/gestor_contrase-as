import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

# Ruta de los scripts
SCRIPTS = {
    "gestor": "./gestor_web/gestor.py",
    "ver_contenido": "./gestor_local/ver_contenido.py",
    "crear_contraseña": "./gestor_local/crear_contraseña_master.py"
}

def ejecutar_script(nombre):
    ruta = SCRIPTS.get(nombre)
    if not ruta or not os.path.isfile(ruta):
        messagebox.showerror("Error", f"No se encontró el archivo '{ruta}'.")
        return
    try:
        subprocess.Popen([sys.executable, ruta])
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo ejecutar '{ruta}':\n{e}")

def salir():
    root.destroy()

# Crear ventana principal
root = tk.Tk()
root.title("Molitalia - Menú Principal")
root.geometry("500x450")
root.configure(bg="#f4f4f4")
root.resizable(False, False)

# Encabezado
tk.Label(root, text="Molitalia", font=("Segoe UI", 24, "bold"), bg="#f4f4f4", fg="#2c3e50").pack(pady=20)
tk.Label(root, text="Panel de Control", font=("Segoe UI", 14), bg="#f4f4f4").pack(pady=5)

# Botones
botones = [
    ("▶️ Iniciar Servidor", lambda: ejecutar_script("gestor"), "#27ae60"),
    ("📂 Ver Contenido", lambda: ejecutar_script("ver_contenido"), "#2980b9"),
    ("🔐 Crear/Modificar Contraseña (MASTER)", lambda: ejecutar_script("crear_contraseña"), "#8e44ad"),
    ("❌ Salir", salir, "#c0392b")
]

for texto, comando, color in botones:
    tk.Button(root, text=texto, command=comando, bg=color, fg="white",
              font=("Segoe UI", 10, "bold"), width=35, height=2).pack(pady=8)

root.mainloop()
