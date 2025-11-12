"""
VULNERABILIDAD: A02 - Cryptographic Failures (OWASP Top 10)
Esta versión contiene MÚLTIPLES fallos criptográficos intencionales para demostración.
NO USAR EN PRODUCCIÓN.
"""

from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import os
import hashlib
import base64

app = Flask(__name__)

# FALLO #1: Secret key predecible y hardcodeada
# Riesgo: Permite a un atacante forjar sesiones y realizar session hijacking
app.secret_key = 'supersecretkey'

# FALLO #2: Clave de cifrado débil y expuesta en el código
ENCRYPTION_KEY = '12345'  # Clave trivial


def weak_encrypt(plaintext):
   """
   FALLO #3: Algoritmo de cifrado débil (XOR simple)
   Riesgo: Fácilmente reversible, no proporciona seguridad real
   """
   key = ENCRYPTION_KEY
   encrypted = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(plaintext))
   return base64.b64encode(encrypted.encode()).decode()


def weak_decrypt(encrypted):
   """Descifrado usando el mismo algoritmo XOR débil"""
   try:
      decoded = base64.b64decode(encrypted).decode()
      key = ENCRYPTION_KEY
      return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(decoded))
   except:
      return None


def weak_hash(password):
   """
   FALLO #4: Uso de MD5 sin salt
   Riesgo: Vulnerable a ataques de rainbow tables y colisiones
   MD5 es criptográficamente inseguro desde 2004
   """
   return hashlib.md5(password.encode()).hexdigest()


def init_db():
   """Inicializa la base de datos"""
   if not os.path.exists('database_vulnerable.db'):
      conn = sqlite3.connect('database_vulnerable.db')
      # FALLO #5: Almacenamiento de datos sensibles sin cifrado
      conn.execute('''CREATE TABLE IF NOT EXISTS users 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password TEXT,
                  email TEXT,
                  credit_card TEXT,
                  ssn TEXT)''')
      
      # Crear usuario de ejemplo (para demostración)
      demo_password = weak_hash('admin123')
      demo_cc = weak_encrypt('4532-1234-5678-9010')
      demo_ssn = weak_encrypt('123-45-6789')
      
      try:
         conn.execute("INSERT INTO users (username, password, email, credit_card, ssn) VALUES (?, ?, ?, ?, ?)",
                  ('admin', demo_password, 'admin@example.com', demo_cc, demo_ssn))
         conn.commit()
      except sqlite3.IntegrityError:
         pass  # Usuario ya existe
      
      conn.close()


@app.route('/')
def index():
   return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
   if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      email = request.form.get('email', '')
      
      # FALLO #6: Hash débil de contraseña (MD5 sin salt)
      hashed_password = weak_hash(password)
      
      # FALLO #7: Datos sensibles cifrados con algoritmo débil
      encrypted_email = weak_encrypt(email) if email else ''
      
      conn = sqlite3.connect('database_vulnerable.db')
      try:
         conn.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                  (username, hashed_password, encrypted_email))
         conn.commit()
         message = "Usuario registrado exitosamente"
      except sqlite3.IntegrityError:
         message = "El usuario ya existe"
      finally:
         conn.close()
      
      return f"<h2>{message}</h2><p><a href='/'>Volver al login</a></p>"
   
   return render_template('register.html')


@app.route('/login', methods=['POST'])
def login():
   username = request.form['username']
   password = request.form['password']
   
   # FALLO #8: Hash de contraseña usando algoritmo débil
   hashed_password = weak_hash(password)
   
   conn = sqlite3.connect('database_vulnerable.db')
   cursor = conn.execute("SELECT * FROM users WHERE username=? AND password=?",
                   (username, hashed_password))
   user = cursor.fetchone()
   conn.close()

   if user:
      # FALLO #9: Almacenamiento de información sensible en sesión
      session['username'] = username
      session['user_id'] = user[0]
      
      # Descifrar email si existe
      decrypted_email = weak_decrypt(user[3]) if user[3] else 'N/A'
      
      return render_template('home.html', user=username, email=decrypted_email)
   else:
      return "<h2>Credenciales inválidas</h2><p><a href='/'>Volver</a></p>"


@app.route('/profile')
def profile():
   """
   FALLO #10: Exposición de datos sensibles sin autenticación adecuada
   """
   if 'username' not in session:
      return redirect('/')
   
   username = session['username']
   conn = sqlite3.connect('database_vulnerable.db')
   cursor = conn.execute("SELECT * FROM users WHERE username=?", (username,))
   user = cursor.fetchone()
   conn.close()
   
   if user:
      # Descifrar datos sensibles
      email = weak_decrypt(user[3]) if user[3] else 'N/A'
      cc = weak_decrypt(user[4]) if user[4] else 'N/A'
      ssn = weak_decrypt(user[5]) if user[5] else 'N/A'
      
      return f"""
      <h2>Perfil de {username}</h2>
      <p><strong>Email:</strong> {email}</p>
      <p><strong>Tarjeta de Crédito:</strong> {cc}</p>
      <p><strong>SSN:</strong> {ssn}</p>
      <p><a href='/'>Inicio</a> | <a href='/db-dump'>Ver Base de Datos (VULNERABLE)</a></p>
      """
   
   return redirect('/')


@app.route('/db-dump')
def db_dump():
   """
   FALLO #11: Exposición completa de la base de datos
   Permite ver contraseñas hasheadas y datos "cifrados"
   """
   conn = sqlite3.connect('database_vulnerable.db')
   cursor = conn.execute("SELECT id, username, password, email, credit_card, ssn FROM users")
   users = cursor.fetchall()
   conn.close()
   
   result = "<h2>VOLCADO DE BASE DE DATOS (VULNERABLE)</h2>"
   result += "<p style='color: red;'>Esta página expone información sensible - Vulnerabilidad crítica</p>"
   result += "<table border='1' cellpadding='10'><tr><th>ID</th><th>Username</th><th>Password Hash (MD5)</th><th>Email (Encrypted)</th><th>Credit Card (Encrypted)</th><th>SSN (Encrypted)</th></tr>"
   
   for user in users:
      result += f"<tr><td>{user[0]}</td><td>{user[1]}</td><td>{user[2]}</td><td>{user[3]}</td><td>{user[4]}</td><td>{user[5]}</td></tr>"
   
   result += "</table><br><p><a href='/'>Volver al inicio</a></p>"
   result += "<h3>Nota para el atacante:</h3>"
   result += "<p>1. Los hashes MD5 pueden crackearse con rainbow tables</p>"
   result += "<p>2. El cifrado XOR es trivialmente reversible</p>"
   result += "<p>3. La clave de cifrado '12345' está en el código fuente</p>"
   
   return result


@app.route('/logout')
def logout():
   session.clear()
   return redirect('/')


if __name__ == '__main__':
   init_db()
   print("\n" + "="*60)
   print("APLICACIÓN VULNERABLE INICIADA")
   print("="*60)
   print("Esta aplicación contiene las siguientes vulnerabilidades:")
   print("1. Secret key predecible y hardcodeada")
   print("2. Clave de cifrado débil expuesta")
   print("3. Algoritmo de cifrado débil (XOR simple)")
   print("4. Uso de MD5 sin salt para passwords")
   print("5. Datos sensibles sin cifrado adecuado en BD")
   print("6-8. Hash débil de contraseñas")
   print("9. Información sensible en sesión")
   print("10-11. Exposición de datos sensibles")
   print("\nUsuario demo: admin / admin123")
   print("Visita /db-dump para ver los datos expuestos")
   print("="*60 + "\n")
   
   # FALLO #12: Debug mode en producción expone información sensible
   app.run(debug=True, host='0.0.0.0', port=5000)
