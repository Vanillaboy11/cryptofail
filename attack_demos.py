"""
🔓 Scripts de Demostración de Ataques
Estos scripts demuestran las vulnerabilidades en la versión 'main'
USO EXCLUSIVO EDUCATIVO
"""

import hashlib
import base64
import requests
import sqlite3

# =============================================================================
# ATAQUE 1: Crackeo de Hash MD5 (Rainbow Table)
# =============================================================================

def crack_md5_local(target_hash, wordlist_file='passwords.txt'):
    """
    Crackea un hash MD5 usando un diccionario local
    
    Args:
        target_hash: Hash MD5 a crackear
        wordlist_file: Archivo con contraseñas comunes
    """
    print(f"[*] Intentando crackear hash: {target_hash}")
    
    # Wordlist común (top 100 passwords)
    common_passwords = [
        'password', '123456', '12345678', 'qwerty', 'abc123',
        'monkey', '1234567', 'letmein', 'trustno1', 'dragon',
        'baseball', '111111', 'iloveyou', 'master', 'sunshine',
        'ashley', 'bailey', 'passw0rd', 'shadow', '123123',
        '654321', 'superman', 'qazwsx', 'michael', 'football',
        'password1', 'admin123', 'admin', 'root', 'toor'
    ]
    
    for password in common_passwords:
        test_hash = hashlib.md5(password.encode()).hexdigest()
        if test_hash == target_hash:
            print(f"[+] ¡CRACKEADO! Password: {password}")
            return password
        
    print(f"[-] Password no encontrado en diccionario básico")
    return None


def demonstrate_md5_collision():
    """
    Demuestra que MD5 permite colisiones
    (dos inputs diferentes con el mismo hash)
    """
    print("\n[*] Demostración de Colisión MD5")
    print("[*] Aunque es difícil generar, MD5 tiene colisiones conocidas")
    print("[*] Ejemplo famoso: shattered.io (Google, 2017)")
    
    # Mismo password, mismo hash (problema sin salt)
    password1 = "admin123"
    password2 = "admin123"
    
    hash1 = hashlib.md5(password1.encode()).hexdigest()
    hash2 = hashlib.md5(password2.encode()).hexdigest()
    
    print(f"\nPassword 1: '{password1}' → Hash: {hash1}")
    print(f"Password 2: '{password2}' → Hash: {hash2}")
    print(f"Hashes iguales: {hash1 == hash2}")
    print("\n[!] Sin salt, usuarios con misma password tienen mismo hash!")


# =============================================================================
# ATAQUE 2: Descifrado XOR
# =============================================================================

def xor_decrypt(encrypted_base64, key='12345'):
    """
    Descifra datos cifrados con XOR simple
    
    Args:
        encrypted_base64: Datos cifrados en base64
        key: Clave XOR (hardcodeada en el código vulnerable)
    """
    print(f"\n[*] Descifrando con clave XOR: '{key}'")
    
    try:
        # Decodificar base64
        decoded = base64.b64decode(encrypted_base64).decode('latin-1')
        
        # Aplicar XOR (reversible)
        decrypted = ''.join(
            chr(ord(c) ^ ord(key[i % len(key)])) 
            for i, c in enumerate(decoded)
        )
        
        print(f"[+] Texto descifrado: {decrypted}")
        return decrypted
        
    except Exception as e:
        print(f"[-] Error al descifrar: {e}")
        return None


def demonstrate_xor_weakness():
    """
    Demuestra por qué XOR no es cifrado seguro
    """
    print("\n[*] Demostración de Debilidad de XOR")
    
    plaintext = "SECRETO"
    key = "12345"
    
    # Cifrar
    encrypted = ''.join(
        chr(ord(c) ^ ord(key[i % len(key)])) 
        for i, c in enumerate(plaintext)
    )
    encrypted_b64 = base64.b64encode(encrypted.encode('latin-1')).decode()
    
    print(f"Texto original: {plaintext}")
    print(f"Cifrado (base64): {encrypted_b64}")
    
    # Descifrar (mismo algoritmo)
    decrypted = xor_decrypt(encrypted_b64, key)
    
    print(f"\n[!] XOR es reversible: A ⊕ B ⊕ B = A")
    print(f"[!] Conociendo la clave, el descifrado es trivial")


# =============================================================================
# ATAQUE 3: SQL Injection para extraer datos (bonus)
# =============================================================================

def demonstrate_timing_attack():
    """
    Demuestra cómo la comparación directa de strings permite timing attacks
    """
    import time
    
    print("\n[*] Demostración de Timing Attack")
    
    # Simulación de verificación vulnerable
    def vulnerable_compare(input_password, stored_password):
        """Comparación insegura - vulnerable a timing attack"""
        if len(input_password) != len(stored_password):
            return False
        for i in range(len(input_password)):
            if input_password[i] != stored_password[i]:
                return False  # Retorna inmediatamente al primer fallo
        return True
    
    # Comparación segura (constant time)
    def secure_compare(input_password, stored_password):
        """Comparación segura - constant time"""
        if len(input_password) != len(stored_password):
            return False
        result = 0
        for i in range(len(input_password)):
            result |= ord(input_password[i]) ^ ord(stored_password[i])
        return result == 0
    
    real_password = "SuperSecret123!"
    
    # Intentar con prefijos cada vez más largos
    attempts = ["S", "Su", "Sup", "Supe", "Super", "Wrong"]
    
    print("\nComparación VULNERABLE (retorna al primer error):")
    for attempt in attempts:
        start = time.perf_counter()
        result = vulnerable_compare(attempt + "x" * (len(real_password) - len(attempt)), 
                                    real_password)
        elapsed = time.perf_counter() - start
        print(f"  '{attempt}...' → {elapsed*1000000:.2f} µs")
    
    print("\n[!] Nota: Tiempos más largos = más caracteres correctos")
    print("[!] Un atacante puede inferir la contraseña caracter por caracter")


# =============================================================================
# ATAQUE 4: Acceso directo a Base de Datos
# =============================================================================

def dump_vulnerable_database(db_path='database_vulnerable.db'):
    """
    Muestra cómo acceder directamente a la BD vulnerable
    """
    print(f"\n[*] Accediendo a base de datos: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.execute("SELECT id, username, password, email FROM users")
        
        print("\n[+] Datos extraídos:")
        print(f"{'ID':<5} {'Usuario':<15} {'Hash MD5':<35} {'Email Cifrado':<20}")
        print("-" * 80)
        
        for row in cursor:
            print(f"{row[0]:<5} {row[1]:<15} {row[2]:<35} {row[3] or 'N/A':<20}")
        
        conn.close()
        
        print("\n[!] Todos los hashes MD5 pueden crackearse con:")
        print("    - CrackStation.net")
        print("    - John the Ripper")
        print("    - Hashcat")
        print("    - Rainbow tables")
        
    except Exception as e:
        print(f"[-] Error: {e}")


# =============================================================================
# ATAQUE 5: Session Hijacking
# =============================================================================

def demonstrate_weak_secret_key():
    """
    Demuestra cómo forjar sesiones con secret key predecible
    """
    print("\n[*] Demostración de Session Forging")
    print("[*] Secret key vulnerable: 'supersecretkey'")
    
    from flask import Flask
    from flask.sessions import SecureCookieSessionInterface
    
    app = Flask(__name__)
    app.secret_key = 'supersecretkey'  # La clave vulnerable
    
    # Crear sesión maliciosa
    session_interface = SecureCookieSessionInterface()
    
    fake_session = {
        'username': 'admin',
        'user_id': 1,
        '_permanent': True
    }
    
    print(f"\n[*] Sesión falsa creada: {fake_session}")
    print("[!] Con la secret key conocida, cualquiera puede:")
    print("    1. Crear sesiones para cualquier usuario")
    print("    2. Modificar datos de sesión existentes")
    print("    3. Escalar privilegios")


# =============================================================================
# CONTRAMEDIDAS (Para comparación)
# =============================================================================

def demonstrate_secure_hashing():
    """
    Muestra cómo se debe hashear correctamente
    """
    from werkzeug.security import generate_password_hash, check_password_hash
    
    print("\n[*] Demostración de Hashing SEGURO")
    
    password = "admin123"
    
    # Generar hash seguro
    secure_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    print(f"\nPassword: {password}")
    print(f"Hash PBKDF2: {secure_hash}")
    print(f"\n[+] Características:")
    print(f"    - Algoritmo: PBKDF2-SHA256")
    print(f"    - Iteraciones: ~260,000")
    print(f"    - Salt: Incluido y aleatorio")
    print(f"    - Longitud: ~90 caracteres")
    
    # Generar otro hash de la misma password
    secure_hash2 = generate_password_hash(password, method='pbkdf2:sha256')
    
    print(f"\n[+] Mismo password, hash diferente:")
    print(f"    Hash 1: {secure_hash[:50]}...")
    print(f"    Hash 2: {secure_hash2[:50]}...")
    print(f"    ¿Iguales? {secure_hash == secure_hash2}")
    
    # Verificar
    print(f"\n[+] Verificación:")
    print(f"    Password correcta: {check_password_hash(secure_hash, 'admin123')}")
    print(f"    Password incorrecta: {check_password_hash(secure_hash, 'wrongpass')}")


def demonstrate_secure_encryption():
    """
    Muestra cómo se debe cifrar correctamente
    """
    from cryptography.fernet import Fernet
    
    print("\n[*] Demostración de Cifrado SEGURO")
    
    # Generar clave
    key = Fernet.generate_key()
    cipher = Fernet(key)
    
    plaintext = "Información Confidencial"
    
    # Cifrar
    encrypted = cipher.encrypt(plaintext.encode())
    
    print(f"\nTexto original: {plaintext}")
    print(f"Clave (base64): {key.decode()}")
    print(f"Cifrado: {encrypted.decode()}")
    
    # Descifrar
    decrypted = cipher.decrypt(encrypted).decode()
    print(f"Descifrado: {decrypted}")
    
    print(f"\n[+] Características de Fernet:")
    print(f"    - Algoritmo: AES-128-CBC")
    print(f"    - Autenticación: HMAC-SHA256")
    print(f"    - Timestamp incluido")
    print(f"    - No reutiliza nonces")
    
    # Intentar con clave incorrecta
    wrong_key = Fernet.generate_key()
    wrong_cipher = Fernet(wrong_key)
    
    try:
        wrong_cipher.decrypt(encrypted)
    except Exception as e:
        print(f"\n[+] Sin la clave correcta: {type(e).__name__}")


# =============================================================================
# MENÚ PRINCIPAL
# =============================================================================

def main():
    """Menú principal para ejecutar demostraciones"""
    
    print("="*80)
    print(" 🎭 DEMOSTRACIÓN DE CRYPTOGRAPHIC FAILURES")
    print("="*80)
    
    while True:
        print("\n[ATAQUES A LA VERSIÓN VULNERABLE]")
        print("1. Crackear hash MD5")
        print("2. Descifrar XOR")
        print("3. Demostrar colisión MD5")
        print("4. Demostrar debilidad XOR")
        print("5. Timing attack")
        print("6. Acceder a base de datos vulnerable")
        print("7. Session hijacking")
        print("\n[CONTRAMEDIDAS - VERSIÓN SEGURA]")
        print("8. Demostrar hashing seguro (PBKDF2)")
        print("9. Demostrar cifrado seguro (Fernet)")
        print("\n0. Salir")
        
        choice = input("\nSeleccione opción: ").strip()
        
        if choice == '1':
            hash_input = input("Ingrese hash MD5 (o Enter para usar ejemplo): ").strip()
            if not hash_input:
                hash_input = "0192023a7bbd73250516f069df18b500"  # admin123
            crack_md5_local(hash_input)
            
        elif choice == '2':
            encrypted = input("Ingrese texto cifrado en base64 (o Enter para ejemplo): ").strip()
            if not encrypted:
                # Ejemplo: "admin@example.com" cifrado con key='12345'
                encrypted = "U0dZXlJeXA=="
            xor_decrypt(encrypted)
            
        elif choice == '3':
            demonstrate_md5_collision()
            
        elif choice == '4':
            demonstrate_xor_weakness()
            
        elif choice == '5':
            demonstrate_timing_attack()
            
        elif choice == '6':
            dump_vulnerable_database()
            
        elif choice == '7':
            demonstrate_weak_secret_key()
            
        elif choice == '8':
            demonstrate_secure_hashing()
            
        elif choice == '9':
            demonstrate_secure_encryption()
            
        elif choice == '0':
            print("\n[*] ¡Hasta luego!")
            break
            
        else:
            print("\n[-] Opción inválida")


if __name__ == '__main__':
    print("\n⚠️  ADVERTENCIA: Este código es solo para fines educativos")
    print("   No usar en sistemas reales sin autorización explícita\n")
    
    main()
