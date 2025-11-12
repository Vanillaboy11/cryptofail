# 🔐 Seminario de Hacking Ético — A02: Cryptographic Failures

## 📋 Descripción del Proyecto
Este proyecto demuestra **múltiples vulnerabilidades criptográficas críticas** (OWASP Top 10 - A02) mediante una aplicación Flask con sistema de autenticación y manejo de datos sensibles.

## 🎯 Objetivos de Aprendizaje
- Identificar fallos criptográficos comunes en aplicaciones web
- Demostrar el impacto real de usar algoritmos débiles
- Implementar soluciones criptográficas robustas
- Comprender la diferencia entre cifrado, hashing y encoding

---

## 🚨 Versión Vulnerable (`main/`)

### Vulnerabilidades Implementadas

#### 1. **Secret Key Predecible**
```python
app.secret_key = 'supersecretkey'  # ❌ Hardcodeada y débil
```
**Impacto**: Session hijacking, forja de tokens

#### 2. **Cifrado XOR Trivial**
```python
def weak_encrypt(plaintext):
    encrypted = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(plaintext))
```
**Impacto**: Fácilmente reversible, sin seguridad real

#### 3. **Hashing MD5 Sin Salt**
```python
def weak_hash(password):
    return hashlib.md5(password.encode()).hexdigest()
```
**Impacto**: Vulnerable a rainbow tables y ataques de colisión

#### 4. **Exposición de Base de Datos**
- Endpoint `/db-dump` expone contraseñas hasheadas
- Datos "cifrados" con XOR son trivialmente reversibles
- Sin control de acceso

#### 5. **Datos Sensibles Expuestos**
- Tarjetas de crédito "cifradas" con XOR
- SSN almacenados con cifrado débil
- Debug mode activado expone stack traces

### Cómo Demostrar el Ataque

1. **Iniciar la versión vulnerable**:
```bash
cd main
python app.py
```

2. **Registrar un usuario**:
   - Ir a http://localhost:5000/register
   - Usuario: `hacker` / Contraseña: `password123`

3. **Acceder al volcado de BD**:
   - Visitar: http://localhost:5000/db-dump
   - ¡Verás todos los hashes MD5 y datos "cifrados"!

4. **Crackear el hash MD5**:
```bash
# Hash MD5 de 'admin123': 0192023a7bbd73250516f069df18b500
# Usar online: https://crackstation.net/
# O con John the Ripper / Hashcat
```

5. **Descifrar datos con XOR**:
```python
# La clave está en el código: ENCRYPTION_KEY = '12345'
# El algoritmo XOR es reversible aplicándolo dos veces
```

---

## ✅ Versión Segura (`fixed/`)

### Soluciones Implementadas

#### 1. **Secret Key Criptográficamente Segura**
```python
app.secret_key = secrets.token_hex(32)  # 256 bits de entropía
```

#### 2. **Derivación de Clave con PBKDF2**
```python
kdf = PBKDF2(
    algorithm=hashes.SHA256(),
    length=32,
    salt=SALT,
    iterations=100000  # NIST recomienda 100k+
)
```

#### 3. **Cifrado AES-256 con Fernet**
```python
cipher_suite = Fernet(get_encryption_key())
encrypted = cipher_suite.encrypt(plaintext.encode())
```
**Ventajas**: Autenticidad + Integridad + Confidencialidad

#### 4. **Hashing PBKDF2-SHA256 con Salt**
```python
hashed = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
verified = check_password_hash(hashed, password)
```

#### 5. **Protecciones Adicionales**
- ✅ Session fixation protection
- ✅ Enmascaramiento de datos sensibles
- ✅ Headers de seguridad HTTP
- ✅ Timing attack protection
- ✅ User enumeration prevention
- ✅ Debug mode deshabilitado

### Demostración de la Defensa

1. **Iniciar versión segura**:
```bash
cd fixed
python app.py
```
(Corre en puerto 5001 por defecto)

2. **Intentar acceder a /db-dump**:
   - Resultado: Error 404 - Endpoint eliminado

3. **Ver contraseñas en BD**:
```bash
sqlite3 database_secure.db "SELECT username, password_hash FROM users;"
```
Resultado:
```
admin|pbkdf2:sha256:260000$randomsalt$longhashvalue...
```
**No se puede crackear**: 100,000 iteraciones + salt único

4. **Intentar descifrar datos sin clave**:
   - Imposible sin la clave derivada
   - AES-256 es estándar militar

---

## 🛠️ Instalación y Ejecución

### Requisitos
- Python 3.8+
- pip

### Setup
```bash
# Clonar el repositorio
git clone <tu-repo>
cd cryptofail

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar versión VULNERABLE (puerto 5000)
cd main
python app.py

# Ejecutar versión SEGURA (puerto 5001)
cd fixed
python app.py
```

### Credenciales de Prueba
- **Usuario**: admin
- **Contraseña**: admin1234

---

## 📊 Comparativa de Seguridad

| Aspecto | VULNERABLE (main) | SEGURO (fixed) |
|---------|-------------------|----------------|
| **Hash de Password** | MD5 sin salt | PBKDF2-SHA256 (100k iter) |
| **Cifrado de Datos** | XOR (clave='12345') | AES-256 (Fernet) |
| **Secret Key** | Hardcodeada | Generada (256 bits) |
| **Derivación de Clave** | Ninguna | PBKDF2-SHA256 |
| **Protección de Sesión** | Ninguna | Regeneración + HTTPOnly |
| **Exposición de Datos** | /db-dump público | Eliminado |
| **Debug Mode** | Activado | Desactivado |
| **Headers de Seguridad** | Ninguno | HSTS, X-Frame, etc. |

---

## 🎓 Conceptos Clave

### Diferencias Importantes

**HASHING** (Contraseñas)
- ❌ MD5, SHA1 → Obsoletos
- ✅ bcrypt, scrypt, Argon2, PBKDF2 → Modernos
- Características: Irreversible, lento intencionalmente, incluye salt

**CIFRADO** (Datos Sensibles)
- ❌ XOR, DES, RC4 → Inseguros
- ✅ AES-256, ChaCha20 → Seguros
- Características: Reversible con clave, rápido, autenticado

**ENCODING** (Transporte)
- Base64, URL encoding → NO ES SEGURIDAD
- Solo para representación, no para protección

### PBKDF2 vs Bcrypt vs Argon2
```
PBKDF2: Estándar NIST, ampliamente compatible
Bcrypt: Popular en Ruby/PHP, resistente a GPU
Argon2: Ganador PHC 2015, resistente a GPU/ASIC
```

---

## 🎤 Estructura de la Presentación

### Acto 1: El Concepto (5 min)
- ¿Qué son las Cryptographic Failures?
- Ejemplos reales: LinkedIn (2012), Adobe (2013)
- Impacto en el OWASP Top 10

### Acto 2: El Ataque en Vivo (10 min)
- Demostración de la app vulnerable
- Acceso a /db-dump
- Crackeo de hash MD5
- Descifrado de datos con XOR

### Acto 3: La Causa Raíz (5 min)
- Análisis del código vulnerable
- Por qué MD5 es inseguro
- Por qué XOR no es cifrado real

### Acto 4: La Solución (10 min)
- Implementación de PBKDF2
- Uso de Fernet (AES-256)
- Demostración de defensa efectiva
- Intentar repetir ataques → FALLA

---

## 📚 Referencias

- [OWASP Top 10 - A02:2021](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)
- [NIST Password Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [Cryptography Library Docs](https://cryptography.io/)
- [Werkzeug Security](https://werkzeug.palletsprojects.com/en/latest/utils/#module-werkzeug.security)

---

## ⚠️ Advertencia Legal

Este proyecto es EXCLUSIVAMENTE para fines educativos. La versión vulnerable (`main/`) contiene fallos de seguridad intencionales y NO debe usarse en producción. El uso indebido de estas técnicas en sistemas sin autorización es ILEGAL.

---

## 👥 Autores
[Tu Equipo Aquí]

## 📝 Licencia
MIT - Uso Educativo
