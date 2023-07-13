from django.db import models  


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Имя покемона')
    title_en = models.CharField(max_length=200, blank=True, null=True, verbose_name='Имя покемона на EN')
    title_jp = models.CharField(max_length=200, blank=True, null=True, verbose_name='Имя покемона на JP')
    image = models.ImageField(blank=True, null=True, verbose_name='Картинка покемона', upload_to='images')
    description = models.TextField(blank=True, null=True, verbose_name='Описание покемона')
    previous_evolution = models.ForeignKey('self',
                                           verbose_name='Из кого эволюционировал',
                                           null=True,
                                           blank=True,
                                           related_name='next_evolutions',
                                           on_delete=models.SET_NULL
                                           )


    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, related_name="entities", on_delete=models.CASCADE, verbose_name='Покемон')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(blank=True, null=True, verbose_name='Время появления')
    disappeared_at = models.DateTimeField(blank=True, null=True, verbose_name='Время изчезновения')
    level = models.IntegerField(null=True, blank=True, verbose_name='Уровень')
    health = models.IntegerField(null=True, blank=True, verbose_name='Здоровье')
    strength = models.IntegerField(null=True, blank=True, verbose_name='Сила')
    defence = models.IntegerField(null=True, blank=True, verbose_name='Защита')
    endurance = models.IntegerField(null=True, blank=True, verbose_name='Выносливость')

    def __str__(self):
        return self.pokemon.title
