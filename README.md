Password Manager es una aplicación de escritorio desarrollada en Python con interfaz gráfica en Tkinter, diseñada para gestionar de forma segura las credenciales de acceso de sistemas internos. Este proyecto está orientado a entornos empresariales que requieren confidencialidad, integridad y control de acceso robusto.

## Características principales
Gestión de contraseñas cifradas con cryptography y argon2.

Verificación de clave maestra antes de acceder a cualquier módulo.

Interfaz empresarial amigable y profesional con Tkinter.

Base de datos SQLite para almacenar credenciales de forma estructurada.

Menú principal con acceso a:

Iniciar servidor (gestor.py)

Visualizar contenido cifrado (ver_contenido.py)

Crear o modificar la contraseña maestra (crear_contraseña_maestra.py)

## Seguridad
Las contraseñas se almacenan cifradas con claves generadas por Fernet.

La clave maestra se protege con hashing Argon2.

Acceso a funciones críticas solo tras autenticación exitosa.

## Requisitos
Python 3.8+

Paquetes:

cryptography

argon2-cffi

tkinter (incluido en la mayoría de instalaciones de Python)

Instala dependencias con:

bash
pip install cryptography argon2-cffi

## Uso
Ejecuta crear_contraseña_maestra.py para establecer la clave maestra.

Inicia el menú principal con menu_principal.py.

Desde el menú puedes iniciar el servidor, ver contenido o modificar la clave.
