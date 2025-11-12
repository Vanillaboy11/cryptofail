import hashlib

print("="*70)
print("CRACKING MD5 HASHES - Demostración de Ataque")
print("="*70)

# Hashes capturados de la base de datos vulnerable
hashes_vulnerables = {
    "admin": "0192023a7bbd73250516f069df18b500",
    "juan": "202cb962ac59075b964b07152d234b70",
    "hacker": "482c811da5d5b4bc6d497ffa98491e38"
}

# Diccionario de contraseñas comunes (top 100 más usadas)
diccionario = [
    "123456", "password", "123456789", "12345678", "12345",
    "1234567", "password1", "123123", "1234567890", "admin",
    "qwerty", "abc123", "111111", "monkey", "letmein",
    "dragon", "master", "sunshine", "princess", "football",
    "admin123", "password123", "welcome", "login", "passw0rd",
    "shadow", "ashley", "bailey", "michael", "jennifer",
    "test", "test123", "pass", "pass123", "superman",
    "qwertyuiop", "654321", "666666", "iloveyou", "trustno1"
]

crackeadas = {}
print("\nIntentando crackear hashes...\n")

for usuario, hash_md5 in hashes_vulnerables.items():
    print(f"Usuario: {usuario}")
    print(f"Hash MD5: {hash_md5}")
    
    for password in diccionario:
        hash_calculado = hashlib.md5(password.encode()).hexdigest()
        if hash_calculado == hash_md5:
            crackeadas[usuario] = password
            print(f"¡CRACKEADA! → '{password}'")
            print()
            break
    else:
        print(f"No encontrada en diccionario básico")
        print(f"Intenta con CrackStation.net: https://crackstation.net/")
        print()

print("RESUMEN")
print(f"Total de hashes: {len(hashes_vulnerables)}")
print(f"Crackeados: {len(crackeadas)}")
print(f"Tiempo estimado: < 1 segundo")
print("\nContraseñas encontradas:")
for usuario, pwd in crackeadas.items():
    print(f"   • {usuario}: {pwd}")

