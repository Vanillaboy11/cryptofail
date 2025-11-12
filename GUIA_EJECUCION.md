# GUÍA DE EJECUCIÓN - Cryptofail Demo

## Scripts Disponibles

### `inspect_db.py` - Ver Bases de Datos
**Qué hace**: Muestra y compara las diferencias entre la BD vulnerable y segura

**Ejecutar**:
```powershell
python inspect_db.py
```

**Output**: Muestra usuarios, hashes, y datos cifrados de ambas versiones


###  `crack_md5.py` - Crackear Hashes MD5
**Qué hace**: Demuestra cómo se pueden romper los hashes MD5 en < 1 segundo

**Ejecutar**:
```powershell
python crack_md5.py
```

**Output**: Recupera las contraseñas originales de los hashes MD5


### `decrypt_xor.py` - Descifrar XOR
**Qué hace**: Descifra tarjetas de crédito, SSN y emails usando la clave XOR hardcodeada

**Ejecutar**:
```powershell
python decrypt_xor.py
```

**Output**: Revela datos sensibles que estaban "cifrados" con XOR


---

## DEMO COMPLETA - Paso a Paso

### FASE 1: Preparar Entorno

**Terminal 1 - App Vulnerable**:
```powershell
cd C:\cryptofail\main
python app.py
```
→ Se ejecuta en http://localhost:5000

**Terminal 2 - App Segura** (opcional):
```powershell
cd C:\cryptofail\fixed
python app.py
```
→ Se ejecuta en http://localhost:5001


### FASE 2: Interactuar con la App

1. **Navegador**: Ir a http://localhost:5000
2. **Login**: `admin` / `admin123`
3. **Ataque**: Ir a http://localhost:5000/db-dump
   - ¡Se expone toda la base de datos!


### FASE 3: Ejecutar Ataques

**En PowerShell**:

```powershell
# Ver las bases de datos
python inspect_db.py

# Crackear hashes MD5
python crack_md5.py

# Descifrar datos XOR
python decrypt_xor.py
```


### FASE 4: Comparar con Versión Segura

1. **Navegador**: Ir a http://localhost:5001/db-dump
   - Resultado: Error 404

2. **Ver BD segura**: Ejecutar `python inspect_db.py`
   - Los hashes son PBKDF2 (imposible crackear)
   - Los datos están cifrados con AES-256


---

## Tabla de Comandos Rápidos

| Acción | Comando | Dónde |
|--------|---------|-------|
| Iniciar app vulnerable | `cd main; python app.py` | Terminal |
| Iniciar app segura | `cd fixed; python app.py` | Terminal |
| Ver bases de datos | `python inspect_db.py` | Terminal |
| Crackear MD5 | `python crack_md5.py` | Terminal |
| Descifrar XOR | `python decrypt_xor.py` | Terminal |
| Probar app | http://localhost:5000 | Navegador |
| Ataque /db-dump | http://localhost:5000/db-dump | Navegador |


---

## Script de Presentación (5 minutos)

### Minuto 1: Introducción
"Les voy a demostrar por qué NO deben usar MD5 ni XOR para seguridad"

### Minuto 2: Mostrar App
- Abrir http://localhost:5000
- Login con `admin` / `admin123`
- "Parece una app normal..."

### Minuto 3: Ataque 1 - Exposición de BD
- Ir a http://localhost:5000/db-dump
- "¡Ups! Puedo ver todos los hashes sin autenticación"

### Minuto 4: Ataque 2 - Cracking
```powershell
python crack_md5.py
```
- "En menos de 1 segundo recuperé 2 contraseñas"

### Minuto 5: Solución
- Mostrar http://localhost:5001
- Intentar /db-dump → Error 404
- Ejecutar `python inspect_db.py`
- "Aquí usamos PBKDF2 + AES-256: imposible de romper"


---

## Troubleshooting

**Error: `ModuleNotFoundError: No module named 'flask'`**
```powershell
pip install -r requirements.txt
```

**Error: `database locked`**
```powershell
# Cerrar las aplicaciones Flask primero (Ctrl+C)
```

**Error: `Address already in use`**
```powershell
# Otro proceso está usando el puerto 5000/5001
# Buscar y cerrar: netstat -ano | findstr :5000
```


---

## Credenciales de Prueba

| Usuario | Contraseña | Ubicación |
|---------|-----------|-----------|
| admin | admin123 | Precreado en ambas BD |
| juan | 123 | Solo en BD vulnerable |
| hacker | password123 | Solo en BD vulnerable |


---

## Recursos Adicionales

- **OWASP A02**: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- **CrackStation**: https://crackstation.net/ (para crackear MD5 online)
- **Documentación Fernet**: https://cryptography.io/en/latest/fernet/
