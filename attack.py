import hashlib

target = "0192023a7bbd73250516f069df18b500" 

# Diccionario de contraseñas comunes
passwords = ["123456", "password", "admin123", "qwerty", "letmein"]

print("Intentando crackear hash MD5... Entrando a la base de datos...")
for pwd in passwords:
    hash_result = hashlib.md5(pwd.encode()).hexdigest()
    if hash_result == target:
        print(f"¡CRACKEADO! Contraseña: {pwd}")
        break
else:
    print("Contraseña no encontrada en diccionario")