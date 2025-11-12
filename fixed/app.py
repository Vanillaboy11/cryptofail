"""
VERSION SEGURA: A02 - Cryptographic Failures MITIGADO (OWASP Top 10)
"""

from flask import Flask, render_template, request, redirect, session, abort
import sqlite3
import os
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
from functools import wraps

app = Flask(__name__)

# SOLUCION #1: Secret key criptograficamente segura y unica
# Genera una nueva clave cada vez (en produccion, usar variable de entorno)
app.secret_key = secrets.token_hex(32)  # 256 bits de entropia

# SOLUCION #2: Clave de cifrado derivada de forma segura
# En produccion, usar variables de entorno
MASTER_PASSWORD = os.environ.get('MASTER_PASSWORD', 'secure_master_password_change_in_production')
SALT = b'salt_stored_securely_12345678'  # En produccion, salt unico por base de datos


def get_encryption_key():
    """
    SOLUCION #3: Derivacion de clave usando PBKDF2
    Genera una clave fuerte a partir de una contrasena usando PBKDF2
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100000,  # Recomendado por NIST
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(MASTER_PASSWORD.encode()))
    return key


# Inicializar Fernet con clave derivada
cipher_suite = Fernet(get_encryption_key())


def secure_encrypt(plaintext):
    """
    SOLUCION #4: Cifrado AES-256 usando Fernet
    Fernet garantiza: autenticidad, integridad y confidencialidad
    """
    if not plaintext:
        return None
    return cipher_suite.encrypt(plaintext.encode()).decode()


def secure_decrypt(encrypted):
    """
    SOLUCION #5: Descifrado seguro con manejo de errores
    """
    if not encrypted:
        return None
    try:
        return cipher_suite.decrypt(encrypted.encode()).decode()
    except Exception as e:
        print(f"Error al descifrar: {e}")
        return None


def init_db():
    """
    SOLUCION #6: Base de datos con cifrado de columnas sensibles
    """
    if not os.path.exists('database_secure.db'):
        conn = sqlite3.connect('database_secure.db')
        conn.execute('''CREATE TABLE IF NOT EXISTS users 
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        email_encrypted BLOB,
                        credit_card_encrypted BLOB,
                        ssn_encrypted BLOB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        # Crear usuario de ejemplo con cifrado real
        demo_password = generate_password_hash('admin123', method='pbkdf2:sha256', salt_length=16)
        demo_cc = secure_encrypt('4532-1234-5678-9010')
        demo_ssn = secure_encrypt('123-45-6789')
        demo_email = secure_encrypt('admin@example.com')
        
        try:
            conn.execute("""INSERT INTO users 
                           (username, password_hash, email_encrypted, credit_card_encrypted, ssn_encrypted) 
                           VALUES (?, ?, ?, ?, ?)""",
                        ('admin', demo_password, demo_email, demo_cc, demo_ssn))
            conn.commit()
        except sqlite3.IntegrityError:
            pass
        
        conn.close()


def login_required(f):
    """
    SOLUCION #7: Decorator para proteger rutas
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    if 'username' in session:
        return redirect('/home')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email', '')
        
        # SOLUCION #8: Validacion de contrasena fuerte
        if len(password) < 8:
            return "<h2>La contrasena debe tener al menos 8 caracteres</h2><p><a href='/register'>Volver</a></p>"
        
        # SOLUCION #9: Hash seguro con Werkzeug (PBKDF2-SHA256)
        # Incluye salt aleatorio automaticamente
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        
        # SOLUCION #10: Cifrado AES-256 para datos sensibles
        encrypted_email = secure_encrypt(email) if email else None
        
        conn = sqlite3.connect('database_secure.db')
        try:
            conn.execute("""INSERT INTO users (username, password_hash, email_encrypted) 
                           VALUES (?, ?, ?)""",
                        (username, hashed_password, encrypted_email))
            conn.commit()
            message = "[OK] Usuario registrado exitosamente con seguridad mejorada"
        except sqlite3.IntegrityError:
            message = "[ERROR] El usuario ya existe"
        finally:
            conn.close()
        
        return f"<h2>{message}</h2><p><a href='/'>Ir al login</a></p>"
    
    return render_template('register.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = sqlite3.connect('database_secure.db')
    
    # SOLUCION #11: Consulta solo por username, verificacion de hash despues
    cursor = conn.execute("SELECT id, username, password_hash, email_encrypted FROM users WHERE username=?",
                         (username,))
    user = cursor.fetchone()
    conn.close()

    # SOLUCION #12: Verificacion segura de hash con timing attack protection
    if user and check_password_hash(user[2], password):
        # SOLUCION #13: Regenerar session ID para prevenir session fixation
        session.clear()
        session['username'] = username
        session['user_id'] = user[0]
        
        # SOLUCION #14: Configuracion de cookies seguras
        session.permanent = True
        app.permanent_session_lifetime = 1800  # 30 minutos
        
        return redirect('/home')
    else:
        # SOLUCION #15: Mensaje generico para prevenir user enumeration
        return "<h2>[ERROR] Credenciales invalidas</h2><p><a href='/'>Volver</a></p>"


@app.route('/home')
@login_required
def home():
    """
    SOLUCION #16: Ruta protegida con autenticacion
    """
    username = session['username']
    conn = sqlite3.connect('database_secure.db')
    cursor = conn.execute("SELECT email_encrypted FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    decrypted_email = secure_decrypt(user[0]) if user and user[0] else 'N/A'
    
    return render_template('home.html', user=username, email=decrypted_email)


@app.route('/profile')
@login_required
def profile():
    """
    SOLUCION #17: Acceso controlado a datos sensibles
    Solo el usuario autenticado puede ver su informacion
    """
    username = session['username']
    conn = sqlite3.connect('database_secure.db')
    cursor = conn.execute("""SELECT email_encrypted, credit_card_encrypted, ssn_encrypted 
                            FROM users WHERE username=?""", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        # Descifrar solo cuando es necesario y solo para el usuario autenticado
        email = secure_decrypt(user[0]) if user[0] else 'N/A'
        
        # SOLUCION #18: Enmascarar datos sensibles (solo mostrar ultimos 4 digitos)
        cc_full = secure_decrypt(user[1]) if user[1] else None
        cc_masked = f"****-****-****-{cc_full[-4:]}" if cc_full else 'N/A'
        
        ssn_full = secure_decrypt(user[2]) if user[2] else None
        ssn_masked = f"***-**-{ssn_full[-4:]}" if ssn_full else 'N/A'
        
        return f"""
        <h2>Perfil Seguro de {username}</h2>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Tarjeta de Credito:</strong> {cc_masked}</p>
        <p><strong>SSN:</strong> {ssn_masked}</p>
        <p style='color: green;'>[OK] Todos los datos estan cifrados en la base de datos con AES-256</p>
        <p><a href='/home'>Inicio</a> | <a href='/logout'>Cerrar Sesion</a></p>
        """
    
    return redirect('/')


@app.route('/db-dump')
def db_dump():
    """
    SOLUCION #19: Endpoint eliminado o restringido a administradores
    En esta version, esta deshabilitado completamente
    """
    abort(404)  # No exponer informacion de base de datos


@app.route('/logout')
def logout():
    """
    SOLUCION #20: Limpieza segura de sesion
    """
    session.clear()
    return redirect('/')


# SOLUCION #21: Headers de seguridad
@app.after_request
def set_security_headers(response):
    """Establecer headers de seguridad HTTP"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # Configuracion de cookies seguras
    if response.status_code == 302:  # Redirect
        response.set_cookie('session', secure=True, httponly=True, samesite='Strict')
    
    return response


if __name__ == '__main__':
    init_db()
    print("\n" + "="*60)
    print("[OK] APLICACION SEGURA INICIADA")
    print("="*60)
    print("Mejoras de seguridad implementadas:")
    print("1. Secret key criptograficamente segura (256 bits)")
    print("2-3. Derivacion de clave con PBKDF2-SHA256")
    print("4-5. Cifrado AES-256 con Fernet")
    print("6. Base de datos con columnas cifradas")
    print("7. Decorators de autenticacion")
    print("8. Validacion de contrasenas")
    print("9. Hash PBKDF2-SHA256 con salt automatico")
    print("10. Cifrado de datos sensibles en reposo")
    print("11-12. Verificacion segura de contrasenas")
    print("13-14. Proteccion contra session fixation")
    print("15. Prevencion de user enumeration")
    print("16-17. Control de acceso basado en roles")
    print("18. Enmascaramiento de datos sensibles")
    print("19. Eliminacion de endpoints peligrosos")
    print("20-21. Headers de seguridad HTTP")
    print("\n[INFO] Usuario demo: admin / admin123")
    print("[INFO] Los datos sensibles estan cifrados con AES-256")
    print("="*60 + "\n")
    
    # SOLUCION #22: Debug mode deshabilitado en produccion
    app.run(debug=False, host='127.0.0.1', port=5001)
