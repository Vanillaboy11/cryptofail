# 🎬 Script de Demostración en Vivo

## Preparación Previa (Antes de la Presentación)

### Setup Inicial
```bash
# Terminal 1 - Versión Vulnerable
cd c:\cryptofail\main
python app.py

# Terminal 2 - Versión Segura  
cd c:\cryptofail\fixed
python app.py
```

### Tener Listas
- Navegador con pestañas: localhost:5000 y localhost:5001
- DB Browser for SQLite (opcional)
- Consola de Python para descifrado

---

## 🎭 ACTO 1: El Concepto (5 minutos)

### Diapositiva 1: Título
**"A02: Cryptographic Failures - Cuando la Criptografía Falla"**

### Diapositiva 2: ¿Qué son?
**Definición:**
> Fallas relacionadas con la criptografía que conducen a la exposición de datos sensibles.

**Incluye:**
- Algoritmos débiles u obsoletos (MD5, DES, RC4)
- Uso inadecuado de criptografía
- Claves hardcodeadas o débiles
- Falta de cifrado en datos sensibles
- Transmisión de datos en texto plano

### Diapositiva 3: Casos Reales
**LinkedIn (2012)**
- 6.5 millones de contraseñas hasheadas con SHA1 sin salt
- Crackeadas en días usando rainbow tables

**Adobe (2013)**
- 150 millones de credenciales
- Passwords cifradas con 3DES en modo ECB (inseguro)
- Misma contraseña = mismo cifrado

**Equifax (2017)**
- Componentes desactualizados
- SSL/TLS mal configurado
- 147 millones de personas afectadas

### Diapositiva 4: Impacto
- 💰 **Financiero**: Multas GDPR hasta €20M o 4% de ingresos
- 🏛️ **Legal**: Demandas colectivas
- 📉 **Reputacional**: Pérdida de confianza
- 🎯 **Personal**: Robo de identidad

---

## 🎭 ACTO 2: El Ataque en Vivo (10 minutos)

### DEMO 1: Registro de Usuario

**Navegador en localhost:5000**

```
👤 NARRADOR:
"Tenemos aquí una aplicación de autenticación aparentemente normal.
Vamos a registrar un usuario..."
```

**Acciones:**
1. Ir a http://localhost:5000/register
2. Llenar formulario:
   - Usuario: `victima`
   - Email: `victima@email.com`
   - Contraseña: `MiPassword2024!`
3. Click "Registrarse"

```
👤 NARRADOR:
"Usuario registrado exitosamente. Todo parece funcionar bien.
Pero... ¿qué está pasando por detrás?"
```

---

### DEMO 2: Exposición de Base de Datos

**Navegador → http://localhost:5000/db-dump**

```
👤 NARRADOR:
"¡Boom! Aquí está el problema. Esta aplicación tiene un endpoint
que expone la base de datos completa."
```

**Señalar en pantalla:**
- Hash MD5 visible: `e10adc3949ba59abbe56e057f20f883e`
- Email "cifrado": `FVdZXlJe`
- Sin autenticación requerida

```
👤 NARRADOR:
"Vemos tres problemas críticos:
1. Contraseñas hasheadas con MD5 - algoritmo obsoleto desde 2004
2. Emails 'cifrados' con XOR - trivialmente reversible
3. Este endpoint no requiere autenticación - ¡cualquiera puede acceder!"
```

---

### DEMO 3: Crackeando MD5

**Abrir nueva pestaña: https://crackstation.net/**

```
👤 NARRADOR:
"MD5 es tan débil que existen bases de datos pre-computadas
llamadas 'rainbow tables'. Vamos a usar una..."
```

**Acciones:**
1. Copiar hash MD5 del usuario admin: `0192023a7bbd73250516f069df18b500`
2. Pegar en CrackStation
3. Click "Crack Hashes"

**Resultado:**
```
Hash: 0192023a7bbd73250516f069df18b500
Type: MD5
Result: admin123
```

```
👤 NARRADOR:
"¡En menos de un segundo! La contraseña es 'admin123'.
Esto es porque MD5:
- Es rápido de calcular (malo para passwords)
- No tiene salt (misma password = mismo hash)
- Existen bases de datos pre-computadas de billones de hashes"
```

---

### DEMO 4: Descifrando XOR

**Abrir consola Python**

```python
import base64

# Datos del db-dump
encrypted_email = "FVdZXlJe"  # Del usuario 'victima'
ENCRYPTION_KEY = "12345"  # ¡Está en el código fuente!

# Descifrar
def xor_decrypt(encrypted, key):
    decoded = base64.b64decode(encrypted).decode()
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(decoded))

result = xor_decrypt(encrypted_email, ENCRYPTION_KEY)
print(f"Email descifrado: {result}")
# Output: victima@email.com
```

```
👤 NARRADOR:
"XOR es una operación reversible. Aplicándola dos veces con la misma clave,
recuperamos el texto original. Además, la clave '12345' está hardcodeada
en el código fuente. ¡No es cifrado real!"
```

---

### DEMO 5: Session Hijacking (Bonus)

**Consola del navegador (F12)**

```javascript
// Ver la cookie de sesión
document.cookie

// Resultado:
// session=eyJ1c2VybmFtZSI6InZpY3RpbWEifQ...
```

```
👤 NARRADOR:
"La secret key 'supersecretkey' es predecible. Un atacante podría
forjar tokens de sesión válidos y hacerse pasar por cualquier usuario."
```

---

## 🎭 ACTO 3: La Causa Raíz (5 minutos)

### Análisis del Código Vulnerable

**Abrir VS Code → main/app.py**

#### Problema 1: Secret Key
```python
app.secret_key = 'supersecretkey'  # ❌ Línea 11
```

```
👤 NARRADOR:
"Esta clave es:
- Predecible (palabra común)
- Hardcodeada en el código
- Igual en todos los despliegues
Un atacante puede forjar sesiones válidas."
```

#### Problema 2: Hash MD5
```python
def weak_hash(password):  # ❌ Línea 34
    return hashlib.md5(password.encode()).hexdigest()
```

```
👤 NARRADOR:
"MD5 es inseguro porque:
- Es muy rápido (GPUs procesan billones/segundo)
- Sin salt: misma password = mismo hash
- Vulnerable a colisiones
- Obsoleto desde 2004"
```

#### Problema 3: XOR "Encryption"
```python
def weak_encrypt(plaintext):  # ❌ Línea 19
    key = ENCRYPTION_KEY  # '12345'
    encrypted = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) 
                       for i, c in enumerate(plaintext))
    return base64.b64encode(encrypted.encode()).decode()
```

```
👤 NARRADOR:
"Esto no es cifrado real:
- XOR es reversible (A ⊕ B ⊕ B = A)
- Clave trivial '12345'
- Sin autenticación del mensaje
- Base64 solo codifica, no cifra"
```

#### Problema 4: DB Dump Público
```python
@app.route('/db-dump')  # ❌ Línea 113
def db_dump():
    # Sin @login_required
    # Sin verificación de permisos
    conn.execute("SELECT * FROM users")
```

```
👤 NARRADOR:
"Este endpoint:
- No requiere autenticación
- Expone todos los datos
- Incluye información 'cifrada' y hasheada
¡Es una mina de oro para atacantes!"
```

---

## 🎭 ACTO 4: La Solución (10 minutos)

### Transición a Versión Segura

```
👤 NARRADOR:
"Ahora veamos cómo un ingeniero de seguridad profesional
resolvería estos problemas."
```

**Navegador → localhost:5001** (versión segura)

---

### SOLUCIÓN 1: Secret Key Segura

**Mostrar código fixed/app.py - Línea 18**

```python
app.secret_key = secrets.token_hex(32)  # ✅ 256 bits de entropía
```

```
👤 NARRADOR:
"Usamos el módulo 'secrets' de Python que genera
claves criptográficamente seguras con 256 bits de entropía.
En producción, esto debería venir de variables de entorno."
```

---

### SOLUCIÓN 2: PBKDF2-SHA256

**Mostrar código fixed/app.py - Línea 131**

```python
hashed_password = generate_password_hash(
    password, 
    method='pbkdf2:sha256',
    salt_length=16
)
```

```
👤 NARRADOR:
"PBKDF2 (Password-Based Key Derivation Function 2) es:
- Estándar NIST
- 100,000 iteraciones por defecto (intencionalmente lento)
- Salt aleatorio único por contraseña
- Resistente a GPUs y ASICs"
```

**Demo: Ver BD Segura**

```bash
sqlite3 database_secure.db "SELECT username, password_hash FROM users LIMIT 1;"
```

**Resultado:**
```
admin|pbkdf2:sha256:260000$aB3dEf$8h9j1k2l3m4n5o6p7q8r9s0t1u2v3w4x...
```

```
👤 NARRADOR:
"Observen:
- 'pbkdf2:sha256' identifica el algoritmo
- '260000' son las iteraciones
- 'aB3dEf' es el salt aleatorio
- El resto es el hash

Cada contraseña tiene su propio salt. Imposible usar rainbow tables."
```

---

### SOLUCIÓN 3: AES-256 con Fernet

**Mostrar código fixed/app.py - Líneas 25-33**

```python
def get_encryption_key():
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100000
    )
    key = base64.urlsafe_b64encode(kdf.derive(MASTER_PASSWORD.encode()))
    return key

cipher_suite = Fernet(get_encryption_key())
```

```
👤 NARRADOR:
"Fernet es una implementación de cifrado autenticado que:
- Usa AES-256 en modo CBC
- Incluye HMAC para autenticación
- Agrega timestamp para validez temporal
- Es el estándar recomendado por cryptography.io"
```

**Mostrar cifrado - Línea 37**

```python
def secure_encrypt(plaintext):
    return cipher_suite.encrypt(plaintext.encode()).decode()
```

**Demo: Intentar descifrar sin clave**

```python
# En consola Python
from cryptography.fernet import Fernet

encrypted = "gAAAAABl..."  # Del database_secure.db
wrong_key = Fernet.generate_key()
cipher = Fernet(wrong_key)

try:
    cipher.decrypt(encrypted.encode())
except Exception as e:
    print(f"Error: {e}")
    # Output: cryptography.fernet.InvalidToken
```

```
👤 NARRADOR:
"Sin la clave correcta, es matemáticamente imposible descifrar.
AES-256 es el estándar usado por agencias gubernamentales."
```

---

### SOLUCIÓN 4: Eliminación de Endpoint Vulnerable

**Intentar acceder: http://localhost:5001/db-dump**

**Resultado: Error 404**

**Mostrar código - Línea 195**

```python
@app.route('/db-dump')
def db_dump():
    abort(404)  # ✅ Endpoint deshabilitado
```

```
👤 NARRADOR:
"Este endpoint no debería existir. Lo eliminamos completamente.
En producción, los accesos a BD requieren:
- Autenticación fuerte
- Autorización basada en roles
- Auditoría de accesos
- Cifrado en tránsito (TLS)"
```

---

### SOLUCIÓN 5: Protecciones Adicionales

**Mostrar headers de seguridad - Línea 203**

```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000'
    # ...
```

```
👤 NARRADOR:
"Agregamos headers de seguridad HTTP que:
- Previenen MIME sniffing
- Protegen contra clickjacking
- Fuerzan HTTPS (HSTS)
- Configuran cookies seguras"
```

---

### DEMO FINAL: Intentar Atacar Versión Segura

**1. Registrar usuario**
```
Usuario: hacker2
Password: password123
```

**2. Intentar acceder a /db-dump**
```
Resultado: 404 Not Found ❌
```

**3. Ver BD directamente**
```bash
sqlite3 database_secure.db "SELECT * FROM users WHERE username='hacker2';"
```

**Resultado:**
```
2|hacker2|pbkdf2:sha256:260000$xyz$abc...|gAAAAABl...|NULL|NULL
```

**4. Intentar crackear en CrackStation**
```
Resultado: No encontrado ❌
```

```
👤 NARRADOR:
"Como pueden ver:
✅ El hash PBKDF2 no aparece en rainbow tables
✅ El cifrado Fernet no puede descifrarse sin clave
✅ El endpoint vulnerable fue eliminado
✅ La aplicación es ahora resistente a estos ataques"
```

---

## 📊 Comparativa Final (Diapositiva)

| Ataque | VULNERABLE | SEGURA |
|--------|-----------|---------|
| Rainbow Tables | ✅ Exitoso | ❌ Bloqueado |
| Descifrado XOR | ✅ Exitoso | ❌ No aplica |
| DB Dump | ✅ Exitoso | ❌ Bloqueado |
| Session Forging | ✅ Posible | ❌ Bloqueado |
| Brute Force | ✅ Rápido | ❌ Muy lento |

---

## 🎯 Conclusiones

### Lecciones Aprendidas

**Para Hashing de Passwords:**
- ❌ MD5, SHA1, SHA256 simple
- ✅ PBKDF2, bcrypt, scrypt, Argon2

**Para Cifrado de Datos:**
- ❌ XOR, DES, 3DES, RC4
- ✅ AES-256, ChaCha20 con autenticación

**Para Secret Keys:**
- ❌ Hardcodeadas, predecibles
- ✅ Generadas aleatoriamente, en variables de entorno

**Para Exposición de Datos:**
- ❌ Endpoints sin autenticación
- ✅ Control de acceso estricto

### Recomendaciones OWASP

1. **Clasificar datos** según sensibilidad
2. **No almacenar datos innecesarios**
3. **Cifrar datos en reposo**
4. **Usar algoritmos modernos**
5. **Gestionar claves apropiadamente**
6. **Deshabilitar caching** para datos sensibles
7. **Aplicar controles de acceso**

---

## ⏱️ Timing del Seminario

- **00:00-05:00**: Acto 1 - Concepto
- **05:00-15:00**: Acto 2 - Ataque en Vivo
- **15:00-20:00**: Acto 3 - Causa Raíz
- **20:00-30:00**: Acto 4 - Solución
- **30:00+**: Preguntas

---

## 🎤 Tips para la Presentación

### Ensayar
- Practicar el flujo completo 2-3 veces
- Tener plan B si falla internet (screenshots)
- Cronometrar cada sección

### Durante la Demo
- Zoom en pantalla para que todos vean
- Narrar lo que haces mientras lo haces
- Pausar para preguntas en cada acto

### Engagement
- Hacer preguntas retóricas al público
- "¿Cuántos creen que esto es seguro?"
- "¿Alguien usa MD5 en sus proyectos?"

### Evitar
- Leer diapositivas palabra por palabra
- Usar jerga excesiva sin explicar
- Apresurarse - tomarse su tiempo

---

## 📝 Checklist Final

**Antes de Presentar:**
- [ ] Ambas apps corriendo (puertos 5000 y 5001)
- [ ] Usuario admin creado en ambas
- [ ] CrackStation.net funcionando
- [ ] VS Code con código abierto
- [ ] DB Browser instalado (opcional)
- [ ] Navegador en modo incógnito (sesión limpia)
- [ ] Terminal preparada
- [ ] Diapositivas listas
- [ ] Cronómetro iniciado

**Durante:**
- [ ] Hablar claro y pausado
- [ ] Mostrar código Y resultado
- [ ] Explicar el "por qué", no solo el "qué"
- [ ] Interactuar con el público

**Después:**
- [ ] Compartir repo de GitHub
- [ ] Responder preguntas
- [ ] Solicitar feedback

---

¡Éxito en su presentación! 🎉
