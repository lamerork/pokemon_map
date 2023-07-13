import datetime
from django.db import models  # noqa F401

# your models here


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Имя покемона')
    image = models.ImageField(blank=True, null=True, verbose_name='Картинка')
    

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(blank=True, null=True, verbose_name='Время появления')
    disappeared_at = models.DateTimeField(blank=True, null=True, verbose_name='Время изчезновения')

    def __str__(self):
        return self.pokemon
