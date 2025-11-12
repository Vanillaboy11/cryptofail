import sqlite3

print("="*70)
print("🔴 BASE DE DATOS VULNERABLE (main/database_vulnerable.db)")
print("="*70)
conn = sqlite3.connect('main/database_vulnerable.db')
cursor = conn.cursor()

cursor.execute("SELECT id, username, password, email, credit_card, ssn FROM users")
rows = cursor.fetchall()

if rows:
    for row in rows:
        print(f"\nUsuario #{row[0]}: {row[1]}")
        print(f"   Email: {row[3] if row[3] else '(vacío)'}")
        print(f"   Password (MD5): {row[2]}")
        print(f"   Tarjeta (XOR): {row[4] if row[4] else '(no registrada)'}")
        print(f"   SSN (XOR): {row[5] if row[5] else '(no registrado)'}")
else:
    print("No hay usuarios registrados. Debes registrar uno primero en http://localhost:5000/register")

conn.close()

print("\n" + "="*70)
print("BASE DE DATOS SEGURA (fixed/database_secure.db)")
print("="*70)
conn = sqlite3.connect('fixed/database_secure.db')
cursor = conn.cursor()

cursor.execute("SELECT id, username, password_hash, email_encrypted, credit_card_encrypted, ssn_encrypted, created_at FROM users")
rows = cursor.fetchall()

if rows:
    for row in rows:
        print(f"\nUsuario #{row[0]}: {row[1]}")
        print(f"   Email: {row[3][:40]}... (Fernet/AES-256)")
        print(f"   Password: {row[2][:60]}...")
        print(f"   ↳ Algoritmo: PBKDF2-SHA256 con 600,000 iteraciones")
        if row[4]:
            print(f"   Tarjeta: {str(row[4])[:40]}... (Fernet/AES-256)")
        if row[5]:
            print(f"   SSN: {str(row[5])[:40]}... (Fernet/AES-256)")
        print(f"   Creado: {row[6]}")
else:
    print("No hay usuarios registrados. Debes registrar uno primero en http://localhost:5001/register")

conn.close()

print("\n" + "="*70)
print("ANÁLISIS DE SEGURIDAD")
print("="*70)
print("VULNERABLE: Columna 'password' usa MD5 (fácil de crackear)")
print("SEGURA: Columna 'password_hash' usa PBKDF2-SHA256 (imposible crackear)")
print("\nVULNERABLE: Email en texto plano")
print("SEGURA: Email cifrado con AES-256")
print("\nVULNERABLE: Tarjeta/SSN cifrados con XOR (trivial de romper)")
print("SEGURA: Tarjeta/SSN cifrados con AES-256 (estándar militar)")
print("="*70)