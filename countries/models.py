from django.db import models
from django.core.exceptions import ValidationError

def validate_positive(value):
    if value is not None and value < 0:
        raise ValidationError('Este valor debe ser positivo.')

class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    official_name = models.CharField(max_length=255, null=True, blank=True)
    flag_png = models.URLField(null=True, blank=True)
    flag_svg = models.URLField(null=True, blank=True)
    capital = models.CharField(max_length=255, null=True, blank=True)
    population = models.BigIntegerField(null=True, blank=True, validators=[validate_positive])
    continents = models.CharField(max_length=255, null=True, blank=True)
    timezones = models.TextField(null=True, blank=True)
    area = models.FloatField(null=True, blank=True, validators=[validate_positive])
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def clean(self):
        if self.latitude is not None and (self.latitude < -90 or self.latitude > 90):
            raise ValidationError({'latitude': 'La latitud debe estar entre -90 y 90.'})
        if self.longitude is not None and (self.longitude < -180 or self.longitude > 180):
            raise ValidationError({'longitude': 'La longitud debe estar entre -180 y 180.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"