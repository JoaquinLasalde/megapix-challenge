import os
from celery import Celery
from celery.schedules import crontab

# Configura la variable de entorno para el módulo de configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'megapix_backend.settings')

app = Celery('megapix_backend')

# Carga la configuración de Celery desde la configuración de Django
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Configura tareas periódicas
app.conf.beat_schedule = {
    'update-countries-every-hour': {
        'task': 'countries.tasks.update_countries',
        'schedule': crontab(minute=0, hour='*'),
    },
}

app.conf.task_acks_late = True
app.conf.task_reject_on_worker_lost = True
app.conf.task_serializer = 'json'