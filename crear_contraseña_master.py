import tkinter as tk
from tkinter import messagebox
from argon2 import PasswordHasher, exceptions as argon2_exceptions
import os
import sys

MASTER_FILE = "./data/master.hash"
os.makedirs(os.path.dirname(MASTER_FILE), exist_ok=True)
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
        messagebox.showinfo("Éxito", "✅ Contraseña maestra actualizada correctamente.")
        root.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al guardar: {e}")

def mostrar_formulario_nueva_contraseña():
    global root, entry_pwd, entry_pwd2
    root = tk.Tk()
    root.title("Molitalia - Nueva Contraseña Maestra")
    root.geometry("400x300")
    root.configure(bg="#f4f4f4")
    root.resizable(False, False)

    tk.Label(root, text="Molitalia", font=("Segoe UI", 20, "bold"), bg="#f4f4f4", fg="#2c3e50").pack(pady=10)
    tk.Label(root, text="Establece una nueva contraseña maestra", font=("Segoe UI", 12), bg="#f4f4f4").pack(pady=5)

    frame = tk.Frame(root, bg="#f4f4f4")
    frame.pack(pady=10)

    tk.Label(frame, text="🔐 Nueva contraseña:", font=("Segoe UI", 10), bg="#f4f4f4").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    entry_pwd = tk.Entry(frame, show="*", width=30)
    entry_pwd.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame, text="🔁 Confirmar:", font=("Segoe UI", 10), bg="#f4f4f4").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_pwd2 = tk.Entry(frame, show="*", width=30)
    entry_pwd2.grid(row=1, column=1, padx=5, pady=5)

    tk.Button(root, text="Guardar Contraseña", command=guardar_contraseña, bg="#2980b9", fg="white", font=("Segoe UI", 10, "bold"), width=25).pack(pady=20)

    root.mainloop()

def verificar_contraseña_actual():
    intento = entry_verificacion.get()
    if not intento:
        messagebox.showwarning("Advertencia", "Por favor, ingresa la contraseña actual.")
        return

    with open(MASTER_FILE, "r") as f:
        hash_guardado = f.read()

    try:
        ph.verify(hash_guardado, intento)
        ventana_verificacion.destroy()
        mostrar_formulario_nueva_contraseña()
    except argon2_exceptions.VerifyMismatchError:
        messagebox.showerror("Acceso denegado", "❌ Contraseña incorrecta.")
        ventana_verificacion.destroy()
        sys.exit()

def mostrar_verificacion():
    global ventana_verificacion, entry_verificacion
    ventana_opciones.destroy()

    ventana_verificacion = tk.Tk()
    ventana_verificacion.title("Molitalia - Verificar Contraseña")
    ventana_verificacion.geometry("400x200")
    ventana_verificacion.configure(bg="#f4f4f4")
    ventana_verificacion.resizable(False, False)

    tk.Label(ventana_verificacion, text="Molitalia", font=("Segoe UI", 20, "bold"), bg="#f4f4f4", fg="#2c3e50").pack(pady=10)
    tk.Label(ventana_verificacion, text="Introduce la contraseña actual", font=("Segoe UI", 12), bg="#f4f4f4").pack(pady=5)

    entry_verificacion = tk.Entry(ventana_verificacion, show="*", width=30, font=("Segoe UI", 10))
    entry_verificacion.pack(pady=10)

    tk.Button(ventana_verificacion, text="Verificar", command=verificar_contraseña_actual, bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold")).pack(pady=10)

    ventana_verificacion.mainloop()

def cerrar_aplicacion():
    ventana_opciones.destroy()
    sys.exit()

# Si ya existe una contraseña, mostrar opciones
if os.path.exists(MASTER_FILE):
    ventana_opciones = tk.Tk()
    ventana_opciones.title("Molitalia - Seguridad")
    ventana_opciones.geometry("400x200")
    ventana_opciones.configure(bg="#f4f4f4")
    ventana_opciones.resizable(False, False)

    tk.Label(ventana_opciones, text="Molitalia", font=("Segoe UI", 20, "bold"), bg="#f4f4f4", fg="#2c3e50").pack(pady=10)
    tk.Label(ventana_opciones, text="⚠️ Ya existe una contraseña maestra configurada.", font=("Segoe UI", 11), bg="#f4f4f4").pack(pady=5)

    tk.Button(ventana_opciones, text="Cambiar contraseña del administrador", command=mostrar_verificacion, bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"), width=30).pack(pady=10)
    tk.Button(ventana_opciones, text="Cerrar", command=cerrar_aplicacion, bg="#c0392b", fg="white", font=("Segoe UI", 10, "bold"), width=30).pack(pady=5)

    ventana_opciones.mainloop()
else:
    mostrar_formulario_nueva_contraseña()
