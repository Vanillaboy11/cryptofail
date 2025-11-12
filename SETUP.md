# 🚀 Setup y Configuración del Proyecto

## Guía Rápida de Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (para clonar el repositorio)

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/cryptofail.git
cd cryptofail
```

### Paso 2: Crear Entorno Virtual (Recomendado)
```bash
# En Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# En Windows (CMD)
python -m venv .venv
.venv\Scripts\activate.bat

# En Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### Paso 3: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Ejecutar Versión Vulnerable
```bash
cd main
python app.py
```
La aplicación estará disponible en: http://localhost:5000

### Paso 5: Ejecutar Versión Segura (en otra terminal)
```bash
cd fixed
python app.py
```
La aplicación estará disponible en: http://localhost:5001

---

## Verificación de Instalación

### Test 1: Verificar que Flask funciona
```bash
python -c "import flask; print('Flask version:', flask.__version__)"
```
Debería mostrar: `Flask version: 3.0.3`

### Test 2: Verificar cryptography
```bash
python -c "from cryptography.fernet import Fernet; print('Cryptography OK')"
```
Debería mostrar: `Cryptography OK`

### Test 3: Ejecutar tests de demo
```bash
python attack_demos.py
```
Debería abrir un menú interactivo.

---

## Estructura del Proyecto

```
cryptofail/
├── main/                      # Versión VULNERABLE
│   ├── app.py                # Aplicación con fallos criptográficos
│   └── templates/            # Plantillas HTML
│       ├── login.html
│       ├── register.html
│       └── home.html
│
├── fixed/                     # Versión SEGURA
│   ├── app.py                # Aplicación con contramedidas
│   └── templates/            # Plantillas HTML
│       ├── login.html
│       ├── register.html
│       └── home.html
│
├── attack_demos.py           # Scripts de demostración de ataques
├── DEMO_SCRIPT.md            # Script detallado para presentación
├── README.md                 # Documentación principal
├── requirements.txt          # Dependencias Python
└── .gitignore               # Archivos ignorados por Git
```

---

## Solución de Problemas Comunes

### Error: "ModuleNotFoundError: No module named 'flask'"
**Solución:**
```bash
pip install flask
```

### Error: "ModuleNotFoundError: No module named 'cryptography'"
**Solución:**
```bash
pip install cryptography
```

### Error: "Address already in use"
**Causa:** El puerto ya está siendo usado por otra aplicación.

**Solución:**
```bash
# Cambiar el puerto en app.py
app.run(debug=True, port=5002)  # Usar otro puerto
```

### Error: "database is locked"
**Causa:** La base de datos está siendo accedida por otra aplicación.

**Solución:**
```bash
# Cerrar todas las conexiones a la BD
# O eliminar el archivo .db y reiniciar la app
```

### Error al activar entorno virtual en PowerShell
**Causa:** Política de ejecución de scripts.

**Solución:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Configuración para Desarrollo

### Habilitar Debug Mode (solo desarrollo)
En `app.py`:
```python
app.run(debug=True, host='127.0.0.1', port=5000)
```

### Cambiar Puerto
```python
app.run(port=8080)  # Usar puerto 8080 en lugar de 5000
```

### Acceder desde otros dispositivos en la red
```python
app.run(host='0.0.0.0', port=5000)
```
**⚠️ ADVERTENCIA:** Solo hacer esto en redes confiables.

---

## Herramientas Adicionales (Opcional)

### DB Browser for SQLite
Para visualizar las bases de datos:
- Descargar: https://sqlitebrowser.org/
- Abrir: `database_vulnerable.db` o `database_secure.db`

### Postman / Insomnia
Para probar API endpoints:
- Postman: https://www.postman.com/
- Insomnia: https://insomnia.rest/

### Burp Suite Community
Para interceptar tráfico HTTP:
- Descargar: https://portswigger.net/burp/communitydownload

---

## Preparación para la Presentación

### Checklist Pre-Demo

1. **Limpiar bases de datos**:
```bash
rm main/database_vulnerable.db
rm fixed/database_secure.db
```

2. **Registrar usuario demo**:
   - Ejecutar `main/app.py`
   - Ir a http://localhost:5000/register
   - Usuario: `admin` / Password: `admin123`
   - Usuario: `victima` / Password: `MiPassword2024!`

3. **Verificar ambas apps**:
   - main en puerto 5000 ✓
   - fixed en puerto 5001 ✓

4. **Tener listo en el navegador**:
   - http://localhost:5000/
   - http://localhost:5000/db-dump
   - http://localhost:5001/
   - https://crackstation.net/

5. **Abrir VS Code con**:
   - `main/app.py`
   - `fixed/app.py`
   - `DEMO_SCRIPT.md`

---

## Comandos Útiles

### Ver logs de la aplicación
```bash
python app.py 2>&1 | tee app.log
```

### Reiniciar base de datos
```bash
# Windows PowerShell
Remove-Item *.db; python app.py

# Linux/Mac
rm *.db && python app.py
```

### Ejecutar en background (Linux/Mac)
```bash
nohup python app.py > app.log 2>&1 &
```

### Ver procesos Flask corriendo
```bash
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000
```

---

## Recursos de Aprendizaje

### OWASP
- Top 10: https://owasp.org/www-project-top-ten/
- Cheat Sheets: https://cheatsheetseries.owasp.org/

### Criptografía
- Cryptography Library: https://cryptography.io/
- NIST Guidelines: https://csrc.nist.gov/publications/

### Python Security
- Bandit: https://bandit.readthedocs.io/
- Safety: https://pyup.io/safety/

### CTF Practice
- OverTheWire: https://overthewire.org/
- HackTheBox: https://www.hackthebox.com/
- PicoCTF: https://picoctf.org/

---

## Contacto y Soporte

Si encuentras problemas:
1. Revisa la sección "Solución de Problemas"
2. Verifica que todas las dependencias estén instaladas
3. Consulta los logs de error
4. Abre un issue en GitHub

---

¡Listo para hackear! 🔐
