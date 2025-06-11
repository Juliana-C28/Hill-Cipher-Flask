#  Hill Cipher Flask App

Aplicación web para cifrar y descifrar resultados médicos utilizando el **cifrado de Hill** con inversión de matrices mediante **métodos iterativos (Jacobi y Gauss-Seidel)**. Desarrollado con **Flask** y desplegado en **Render.com**.



##  Caso de uso

En entornos médicos como hospitales, clínicas rurales o campañas de salud, los resultados de exámenes pueden transmitirse sin seguridad. Esta app permite cifrarlos para:

- Evitar divulgación sin consentimiento.
- Proteger la privacidad del paciente.
- Garantizar la integridad de la información médica.

---

##  Funcionalidades

-  Generación automática de matrices clave válidas.
-  Cifrado de diagnósticos (los espacios se reemplazan por `'X'`).
-  Descifrado usando inversión iterativa de la matriz.
-  Métodos Jacobi y Gauss-Seidel para la inversión.
-  Visualización de iteraciones y verificación modular.

##  Tecnologías

- Python 3.11  
- Flask 2.2.5  
- NumPy 1.26.4  
- HTML, CSS, JavaScript  
- Plantillas Jinja2  


##  Estructura del proyecto

hill_cipher_app/
├── backend/
│   ├── app.py
│   └── templates/
│       └── index.html
├── requirements.txt
├── start.sh
├── render.yaml

##  Cómo ejecutar localmente

1. Clona el repositorio:

   `git clone https://github.com/tu-usuario/hill-cipher-flask.git`

2. Entra en el directorio:

   `cd hill-cipher-flask`

3. Instala dependencias:

   `pip install -r requirements.txt`

4. Ejecuta la app:

   `python backend/app.py`

Visita `http://localhost:5000` en tu navegador.

##  Despliegue en Render

Este proyecto está preparado para **Render.com** mediante el siguiente archivo de configuración:

### `render.yaml`

```yaml
services:
  - type: web
    name: hill-cipher-flask
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "bash start.sh"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11
```

- Cada push a la rama `main` activa el build automáticamente.
- La URL pública será algo como:  
  `https://hill-cipher-flask.onrender.com`

## Enlace de render 
https://hill-cipher-flask.onrender.com/


## 👨‍⚕️ Desarrollado por

*Juliana Casas Ramirez
*Natalia Florez Guzman

Aplicación con fines académicos y de protección de datos médicos sensibles.



## 🛡 Licencia

MIT License — Puedes usar, modificar y distribuir libremente con atribución.
