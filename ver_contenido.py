import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import os
import sys

# Verificación de clave maestra
from seguridad import verificar_clave_maestra
verificar_clave_maestra()

DB_PATH = "data.db"

if not os.path.isfile(DB_PATH):
    messagebox.showerror("Molitalia - Error", f"BD no encontrada'{DB_PATH}'.")
    sys.exit()

# Conexión a la base de datos
try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username, pwd_hash FROM users")
    filas = cursor.fetchall()
    conn.close()
except sqlite3.OperationalError as e:
    messagebox.showerror("Molitalia - Error", f"Error al acceder a la BD:\n{e}")
    sys.exit()

# Crear ventana principal
root = tk.Tk()
root.title("Molitalia - Usuarios Registrados")
root.geometry("600x400")
root.configure(bg="#f4f4f4")

tk.Label(root, text="Molitalia", font=("Segoe UI", 20, "bold"), bg="#f4f4f4", fg="#2c3e50").pack(pady=10)
tk.Label(root, text="Usuarios registrados en el sistema web", font=("Segoe UI", 12), bg="#f4f4f4").pack(pady=5)

# Tabla para mostrar usuarios
columns = ("usuario", "hash")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
tree.heading("usuario", text="👤 Usuario")
tree.heading("hash", text="🔐 Hash de Contraseña")

# Estilo empresarial
style = ttk.Style()
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

# Insertar datos
if not filas:
    messagebox.showinfo("Molitalia - Información", "No hay usuarios registrados.")
else:
    for username, pwd_hash in filas:
        tree.insert("", "end", values=(username, pwd_hash))

tree.pack(padx=20, pady=10, fill="both", expand=True)

# Botón para cerrar
tk.Button(root, text="Cerrar", command=root.destroy, bg="#c0392b", fg="white", font=("Segoe UI", 10, "bold")).pack(pady=10)

root.mainloop()
