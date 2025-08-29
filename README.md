# BACKEND SISTEMA DE MESA DE PARTES

El Sistema de Mesa de Partes es una aplicación web que permite la recepción, registro, gestión y seguimiento de trámites o solicitudes de documentos en línea.
Los usuarios pueden enviar sus documentos de forma digital, mientras que los administradores pueden revisarlos, responderlos y dar seguimiento al estado del trámite (pendiente, en proceso o atendido).

## ⚙️ Instalación
Seguir los siguientes comandos en una terminal para levantar el proyecto (tener isntalado git y python), se recomienda estar en alguna distribución de linux y tener instalado mysql

```bash
git clone https://github.com/ampuero11/mesa_tramites_Backend
```

```bash
cd mesa_tramites_Backend
```

```bash
code .
```

Se debe crear un entorno virtual, si ya lo tienes debes activarlo

```bash
python3 -m venv env
```

```bash
./venv/Scripts/activate  # On Linux use:  source venv/bin/activate     
```

Instalar los paquetes

```bash
pip install -r requirements.txt 
```

Levantar el proyecto
antes de levantar el proyecto es importante crear la base de datos en mysql de nombre mesa_de_partes_db, y configurar mesa_partes/settings.py linea 87, DATABSES
colocar los atributos correspondientes, USER, PASSWORDM HOST, Y PORT, según su sistema, caso contrario reemplazar el bloque de DATABASES Por el siguiente codigo

```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}
```

Una vez confirgurado la base de datos, correr el proyecto

```bash
cd mesa_partes
```

Sí es la primera vez, realizar migraciones

```bash
python3 manage.py makemigrations
```

```bash
python3 manage.py migrate
```
Levantar servidor

```bash
python3 manage.py runserver
```

Si necesitas crear un usuario para el administrador, sigue los siguientes pasos

```bash
python3 manage.py createsuperuser
```

y seguir los pasos, no olvidar estar en al carpeta mesa_partes cuando usamos comandos con manage.py
