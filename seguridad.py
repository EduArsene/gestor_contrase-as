import tkinter as tk
from tkinter import messagebox
from argon2 import PasswordHasher, exceptions as argon2_exceptions
import os
import sys

MASTER_FILE = "./data/master.hash"

def verificar_clave_maestra():
    if not os.path.isfile(MASTER_FILE):
        messagebox.showerror("Molitalia - Seguridad", "No existe una clave maestra.\nEjecuta primero la configuración inicial.")
        sys.exit()

    def verificar():
        intento = entry_pwd.get()
        if not intento:
            messagebox.showwarning("Advertencia", "Por favor, ingresa la contraseña.")
            return

        with open(MASTER_FILE, "r") as f:
            hash_guardado = f.read()

        ph = PasswordHasher()
        try:
            ph.verify(hash_guardado, intento)
            messagebox.showinfo("Acceso concedido", "Clave maestra correcta.")
            ventana.destroy()
        except argon2_exceptions.VerifyMismatchError:
            messagebox.showerror("Acceso denegado", "Clave maestra incorrecta.")
            ventana.destroy()
            sys.exit()

    def al_cerrar():
        # Si el usuario intenta cerrar la ventana sin verificar, se cierra toda la app
        messagebox.showwarning("Molitalia - Seguridad", "Debes ingresar la contraseña maestra para continuar.")
        ventana.destroy()
        sys.exit()

    # Ventana de ingreso
    ventana = tk.Tk()
    ventana.title("Molitalia - Verificación de Clave Maestra")
    ventana.geometry("400x200")
    ventana.configure(bg="#f4f4f4")
    ventana.resizable(False, False)

    # Bloquear el botón de cerrar
    ventana.protocol("WM_DELETE_WINDOW", al_cerrar)

    tk.Label(ventana, text="Molitalia", font=("Segoe UI", 20, "bold"), bg="#f4f4f4", fg="#2c3e50").pack(pady=10)
    tk.Label(ventana, text="Introduce la contraseña maestra", font=("Segoe UI", 12), bg="#f4f4f4").pack(pady=5)

    entry_pwd = tk.Entry(ventana, show="*", width=30, font=("Segoe UI", 10))
    entry_pwd.pack(pady=10)

    btn_verificar = tk.Button(ventana, text="Verificar", command=verificar, bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"))
    btn_verificar.pack(pady=10)

    ventana.mainloop()
