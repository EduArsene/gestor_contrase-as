import tkinter as tk
from tkinter import messagebox
from argon2 import PasswordHasher
import os

MASTER_FILE = "./data/master.hash"

# Crear carpeta si no existe
os.makedirs(os.path.dirname(MASTER_FILE), exist_ok=True)

# Verificar si ya existe una contraseña maestra
if os.path.exists(MASTER_FILE):
    messagebox.showwarning("Molitalia - Seguridad", "⚠️ Ya existe una contraseña maestra configurada.")
    exit()

ph = PasswordHasher()

def guardar_contraseña():
    pwd = entry_pwd.get()
    pwd2 = entry_pwd2.get()

    if not pwd or not pwd2:
        messagebox.showerror("Error", "Por favor, completa ambos campos.")
        return

    if pwd != pwd2:
        messagebox.showerror("Error", "❌ Las contraseñas no coinciden.")
        return

    try:
        hashed = ph.hash(pwd)
        with open(MASTER_FILE, "w") as f:
            f.write(hashed)
        messagebox.showinfo("Éxito", "Contraseña maestra guardada correctamente.")
        root.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al guardar: {e}")

# Crear ventana principal
root = tk.Tk()
root.title("Molitalia - Configurar Contraseña Maestra")
root.geometry("400x300")
root.resizable(False, False)
root.configure(bg="#f4f4f4")

# Estilo empresarial
tk.Label(root, text="Molitalia", font=("Segoe UI", 20, "bold"), bg="#f4f4f4", fg="#2c3e50").pack(pady=10)
tk.Label(root, text="Configura tu contraseña maestra", font=("Segoe UI", 12), bg="#f4f4f4").pack(pady=5)

frame = tk.Frame(root, bg="#f4f4f4")
frame.pack(pady=10)

tk.Label(frame, text="🔐 Contraseña:", font=("Segoe UI", 10), bg="#f4f4f4").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_pwd = tk.Entry(frame, show="*", width=30)
entry_pwd.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="🔁 Confirmar:", font=("Segoe UI", 10), bg="#f4f4f4").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_pwd2 = tk.Entry(frame, show="*", width=30)
entry_pwd2.grid(row=1, column=1, padx=5, pady=5)

btn_guardar = tk.Button(root, text="Guardar Contraseña", command=guardar_contraseña, bg="#2980b9", fg="white", font=("Segoe UI", 10, "bold"), width=25)
btn_guardar.pack(pady=20)

root.mainloop()
