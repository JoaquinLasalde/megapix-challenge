import time
import requests
from celery import shared_task
from django.core.cache import cache
from django.db import transaction, IntegrityError, OperationalError
from .models import Country
from celery.utils.log import get_task_logger
from requests.exceptions import RequestException, Timeout, HTTPError

logger = get_task_logger(__name__)

LOCK_EXPIRE = 60 * 60  # 1 hora
COOLDOWN_TIME = 60 * 5  # 5 minutos

@shared_task(bind=True, max_retries=3)
def update_countries(self):
    lock_id = "update_countries_lock"
    
    # Intenta adquirir un bloqueo para evitar ejecuciones simultáneas
    acquired = cache.add(lock_id, "lock", LOCK_EXPIRE)
    if not acquired:
        logger.info("La tarea ya está en ejecución. Saltando esta ejecución.")
        return "La tarea ya está en ejecución. Ejecución saltada."

    try:
        # Verifica si la tarea se ejecutó recientemente
        last_run = cache.get("last_update_countries_run")
        if last_run and time.time() - float(last_run) < COOLDOWN_TIME:
            logger.info("La tarea se ejecutó recientemente. Saltando debido al tiempo de espera.")
            return "Tarea saltada debido al tiempo de espera"

        # URL de la API externa para obtener datos de países
        url = "https://restcountries.com/v3.1/all?fields=name,flags,capital,population,continents,timezones,area,latlng"
        
        try:
            # Realiza la solicitud a la API externa
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            countries_data = response.json()
        except Timeout:
            logger.error("Tiempo de espera agotado al conectar con la API externa.")
            raise self.retry(countdown=60)
        except HTTPError as http_err:
            logger.error(f"Error HTTP al conectar con la API externa: {http_err}")
            raise self.retry(countdown=60)
        except RequestException as req_err:
            logger.error(f"Error al conectar con la API externa: {req_err}")
            raise self.retry(countdown=60)

        # Actualiza la base de datos con los nuevos datos de países
        with transaction.atomic():
            try:
                for country_data in countries_data:
                    country, created = Country.objects.update_or_create(
                        name=country_data['name']['common'],
                        defaults={
                            'official_name': country_data['name'].get('official'),
                            'flag_png': country_data['flags'].get('png'),
                            'flag_svg': country_data['flags'].get('svg'),
                            'capital': ', '.join(country_data.get('capital', [])),
                            'population': country_data.get('population'),
                            'continents': ', '.join(country_data.get('continents', [])),
                            'timezones': ', '.join(country_data.get('timezones', [])),
                            'area': country_data.get('area'),
                            'latitude': country_data['latlng'][0] if len(country_data.get('latlng', [])) > 0 else None,
                            'longitude': country_data['latlng'][1] if len(country_data.get('latlng', [])) > 1 else None,
                        }
                    )
                    if created:
                        logger.info(f"País creado: {country.name}")
                    else:
                        logger.info(f"País actualizado: {country.name}")          
                        
            except IntegrityError as ie:
                logger.error(f"Error de integridad al guardar los datos: {ie}")
                raise
            except OperationalError as oe:
                logger.error(f"Error operacional con la base de datos: {oe}")
                raise self.retry(countdown=60)
        
        # Actualiza el tiempo de la última ejecución exitosa
        cache.set("last_update_countries_run", str(time.time()), COOLDOWN_TIME)
        
        logger.info(f"Se actualizaron exitosamente {len(countries_data)} países")
        return f"Se actualizaron exitosamente {len(countries_data)} países"
    
    except Exception as e:
        logger.error(f"Error al actualizar países: {str(e)}")
        raise self.retry(exc=e, countdown=60)
    finally:
        # Libera el bloqueo al finalizar
        cache.delete(lock_id)