import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from cryptography.fernet import Fernet
import os

# Verificación de clave maestra
from seguridad import verificar_clave_maestra
verificar_clave_maestra()

# Cargar clave de cifrado
try:
    with open("./key.key", "rb") as f:
        clave = f.read()
    fernet = Fernet(clave)
except FileNotFoundError:
    messagebox.showerror("Error", "No se encontró el archivo de clave de cifrado.")
    exit()

# Conectar a la base de datos
try:
    conn = sqlite3.connect("./database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT sitio, usuario, contrasena FROM contrasenas")
    filas = cursor.fetchall()
    conn.close()
except Exception as e:
    messagebox.showerror("Error", f"No se pudo acceder a la base de datos: {e}")
    exit()

# Crear ventana principal
root = tk.Tk()
root.title("Molitalia - Gestor de Contraseñas")
root.geometry("600x400")
root.configure(bg="#f4f4f4")

tk.Label(root, text="Molitalia", font=("Segoe UI", 20, "bold"), bg="#f4f4f4", fg="#2c3e50").pack(pady=10)
tk.Label(root, text="Credenciales almacenadas (modo seguro)", font=("Segoe UI", 12), bg="#f4f4f4").pack(pady=5)

# Tabla para mostrar datos
columns = ("sitio", "usuario", "contrasena")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
tree.heading("sitio", text="🧾 Sitio")
tree.heading("usuario", text="👤 Usuario")
tree.heading("contrasena", text="🔐 Contraseña (cifrada)")

# Estilo empresarial
style = ttk.Style()
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

# Insertar datos
for sitio, usuario, contrasena_cifrada in filas:
    try:
        tree.insert("", "end", values=(sitio, usuario, contrasena_cifrada.decode()))
    except Exception:
        tree.insert("", "end", values=(sitio, usuario, "❌ Error al descifrar"))

tree.pack(padx=20, pady=10, fill="both", expand=True)

# Botón para cerrar
tk.Button(root, text="Cerrar", command=root.destroy, bg="#c0392b", fg="white", font=("Segoe UI", 10, "bold")).pack(pady=10)

root.mainloop()
