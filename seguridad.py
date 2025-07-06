from argon2 import PasswordHasher, exceptions as argon2_exceptions
import getpass
import os

MASTER_FILE = "./data/master.hash"

def verificar_clave_maestra():
    if not os.path.isfile(MASTER_FILE):
        print("❌ No existe una clave maestra. Ejecuta primero crear_contraseña_maestra.py")
        exit()

    with open(MASTER_FILE, "r") as f:
        hash_guardado = f.read()

    intento = getpass.getpass("🔐 Introduce la contraseña maestra: ")
    ph = PasswordHasher()
    try:
        ph.verify(hash_guardado, intento)
        print("✅ Clave maestra correcta.")
    except argon2_exceptions.VerifyMismatchError:
        print("❌ Clave maestra incorrecta.")
        exit()
