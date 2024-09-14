# Megapix Challenge
Este proyecto es una API REST desarrollada con Django y Django REST Framework que consume datos de países desde una API externa y los almacena en una base de datos local (postgreSQL). Utiliza Celery para tareas programadas y está completamente dockerizado para facilitar su despliegue y ejecución.

## Instrucciones para levantar el entorno desde cero de manera local
Siga estos pasos para configurar y ejecutar el proyecto:

### 1. Clonar el repositorio
```bash
git clone https://github.com/JoaquinLasalde/megapix-challenge.git
cd megapix-challenge
```

### 2. Configurar las variables de entorno
Cree un archivo `.env` en la raíz del proyecto:

Abra el archivo `.env` y configure las variables con sus valores deseados:

```
POSTGRES_DB=megapix_db
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
CELERY_BROKER=redis://redis:6379/0
CELERY_BACKEND=redis://redis:6379/0
```

Asegúrese de cambiar `your_username` y `your_password` por valores seguros de su elección.

### 3. Construir y levantar el entorno utilizando Docker
```bash
docker-compose up --build -d
```
Este comando construirá las imágenes necesarias y levantará los contenedores en modo detached. Los servicios que se iniciarán son:
- Django web server
- PostgreSQL database
- Redis (para Celery)
- Celery worker
- Celery beat (para tareas programadas)

Una vez que los contenedores estén en funcionamiento, ejecute las migraciones de Django:
```bash
docker-compose exec web python manage.py migrate
```

### 4. Ejecutar la tarea programada
La tarea para consumir los datos de los países está configurada para ejecutarse automáticamente cada hora. Sin embargo, se puede ejecutar manualmente con el siguiente comando:
```bash
docker-compose exec web python manage.py shell -c "from countries.tasks import update_countries; update_countries.delay()"
```
(tener en cuenta que existe un cooldown de 5 minutos)

### 5. Acceder al endpoint REST
Una vez que el proyecto esté en funcionamiento y la base de datos poblada, puede acceder al endpoint REST para listar los países:
- Lista de países: `http://localhost:8000/api/countries/`
- Detalles de un país específico: `http://localhost:8000/api/countries/{id}/`

El endpoint soporta paginación y filtrado. Algunos ejemplos de uso:
- Filtrar por nombre: `http://localhost:8000/api/countries/?name=Spain`
- Filtrar por población: `http://localhost:8000/api/countries/?population_gt=1000000`
- Filtrar por continente: `http://localhost:8000/api/countries/?continent=Europe`

## Notas adicionales
- El proyecto utiliza Docker y Docker Compose, asegúrese de tenerlos instalados en su sistema antes de comenzar.
- La única dependencia externa del proyecto es el endpoint de `restcountries.com`, que se utiliza para obtener los datos de los países.
- Si encuentra algún problema durante la configuración o ejecución, verifique los logs de los contenedores usando `docker-compose logs [service_name]`.
