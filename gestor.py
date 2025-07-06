from flask import Flask, render_template_string, request, redirect, url_for, session, flash
import sqlite3, os
from argon2 import PasswordHasher
from cryptography.fernet import Fernet

# ─── Configuración ────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'data.db')
KEY_PATH = os.path.join(BASE_DIR, 'key.key')

# Generar o cargar clave Fernet
if not os.path.isfile(KEY_PATH):
    with open(KEY_PATH, 'wb') as f:
        f.write(Fernet.generate_key())
fernet = Fernet(open(KEY_PATH,'rb').read())

# Inicializar Argon2 hasher
ph = PasswordHasher()

# Crear DB y tabla de usuarios si no existen
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                pwd_hash TEXT NOT NULL
            )''')
conn.commit()
conn.close()

app = Flask(__name__)
app.secret_key = os.urandom(16)  # para sesiones de Flask

# ─── Plantillas HTML (inline para brevedad) ────────────────────────────────────

LOGIN_HTML = """
<!doctype html><title>Login Seguro</title>
<h2>Login</h2>
<form method=post>
  Usuario: <input name=username><br>
  Contraseña: <input type=password name=password><br>
  <button type=submit>Entrar</button>
</form>
<p>¿No tienes cuenta? <a href="{{ url_for('register') }}">Regístrate</a></p>
{% with msg = get_flashed_messages() %}
  {% if msg %}<p style="color:red;">{{ msg[0] }}</p>{% endif %}
{% endwith %}
"""

REGISTER_HTML = """
<!doctype html><title>Registro</title>
<h2>Registro</h2>
<form method=post>
  Usuario: <input name=username><br>
  Contraseña: <input type=password name=password><br>
  <button type=submit>Crear cuenta</button>
</form>
<p><a href="{{ url_for('login') }}">Volver a login</a></p>
{% with msg = get_flashed_messages() %}
  {% if msg %}<p style="color:red;">{{ msg[0] }}</p>{% endif %}
{% endwith %}
"""

DASH_HTML = """
<!doctype html><title>Panel</title>
<h2>Bienvenido, {{ session['user'] }}!</h2>
<p>Este mensaje está cifrado con Fernet:</p>
<pre>{{ token }}</pre>
<p><a href="{{ url_for('logout') }}">Salir</a></p>
"""

# ─── Rutas ───────────────────────────────────────────────────────────────────

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        u = request.form['username'].strip()
        p = request.form['password']
        if not u or not p:
            flash("Usuario y contraseña obligatorios.")
        else:
            try:
                hash = ph.hash(p)
                conn = sqlite3.connect(DB_PATH)
                conn.execute("INSERT INTO users (username,pwd_hash) VALUES (?,?)", (u, hash))
                conn.commit()
                conn.close()
                flash("Cuenta creada. ¡Puedes iniciar sesión!")
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash("El usuario ya existe.")
    return render_template_string(REGISTER_HTML)

@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username'].strip()
        p = request.form['password']
        conn = sqlite3.connect(DB_PATH)
        row = conn.execute("SELECT pwd_hash FROM users WHERE username=?", (u,)).fetchone()
        conn.close()
        if row:
            try:
                ph.verify(row[0], p)
                session['user'] = u
                # Generar token cifrado de bienvenida
                token = fernet.encrypt(f"Usuario {u} autenticado.".encode()).decode()
                return render_template_string(DASH_HTML, token=token)
            except:
                flash("Usuario o contraseña inválidos.")
        else:
            flash("Usuario o contraseña inválidos.")
    return render_template_string(LOGIN_HTML)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ─── Arranque con HTTPS de desarrollo ─────────────────────────────────────────

if __name__ == '__main__':
    # Con SSL auto-generado para desarrollo
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
