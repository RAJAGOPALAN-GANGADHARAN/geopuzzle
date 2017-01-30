from django.contrib.gis.db.models import MultiPointField
from django.contrib.gis.db.models import MultiPolygonField
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import MultiPoint
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import JSONField
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.functional import cached_property
from hvad.models import TranslatableModel, TranslatedFields

from maps.converter import encode_coords
from maps.infobox import query

DIFFICULTY_LEVELS = (
    (0, 'disabled'),
    (1, 'easy'),
    (2, 'normal'),
    (3, 'hard'),
)

ZOOMS = (
    (3, 'world'),
    (4, 'large country'),
    (5, 'big country'),
    (6, 'country'),
    (7, 'small country'),
    (8, 'little country'),
    (9, 'region'),
)


class Country(TranslatableModel):
    image = models.ImageField(upload_to='countries', blank=True)
    slug = models.CharField(max_length=15, db_index=True)
    center = PointField(geography=True)
    position = PointField(geography=True)
    zoom = models.PositiveSmallIntegerField(choices=ZOOMS)
    default_count = models.PositiveSmallIntegerField(default=0)
    sparql = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(default=False)

    translations = TranslatedFields(
        name = models.CharField(max_length=15)
    )

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.safe_translation_getter('name', str(self.pk))

    def get_absolute_url(self):
        return reverse('maps_map', args=(self.slug,))

    def get_init_params(self):
        return {
            'zoom': self.zoom,
            'position': list(self.position.coords),
            'center': list(self.center.coords)
        }


class Area(TranslatableModel):
    country = models.ForeignKey(Country)
    difficulty = models.PositiveSmallIntegerField(choices=DIFFICULTY_LEVELS, default=0)
    polygon = MultiPolygonField(geography=True)
    answer = MultiPointField(geography=True, null=True)

    translations = TranslatedFields(
        name = models.CharField(max_length=50),
        infobox = JSONField(null=True, blank=True)
    )

    caches = {
        'polygon_gmap': 'area{id}gmap'
    }

    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'

    def __str__(self):
        return self.safe_translation_getter('name', str(self.pk))

    def get_absolute_url(self):
        return '{}?id={}'.format(reverse('maps_map', args=(self.country.slug,)), self.id)

    @property
    def polygon_gmap(self):
        # http://lists.osgeo.org/pipermail/postgis-users/2007-February/014612.html
        cache_key = self.caches['polygon_gmap'].format(id=self.id)
        result = cache.get(cache_key)
        if result is None:
            result = []
            for polygon in self.polygon:
                result.append(encode_coords(polygon.coords[0]))
                if len(polygon.coords) > 1:
                    result.append(encode_coords(polygon.coords[1]))
            cache.set(cache_key, result, timeout=None)
        return result

    def update_infobox(self):
        for language in self.get_available_languages():
            obj = Area.objects.language(language).get(pk=self.pk)
            obj.infobox = query(self.country.sparql, language=language, name=obj.safe_translation_getter('name', ''))
            obj.save()

    def recalc_answer(self):
        diff = (-1, -1, 1, 1)
        extent = self.polygon.extent
        scale = 1.0 / (self.country.zoom - 2)
        points = [extent[i] + diff[i] * scale for i in range(4)]
        self.answer = MultiPoint(Point(points[0], points[1]), Point(points[2], points[3]))
        self.save()


@receiver(post_save, sender=Area, dispatch_uid="clear_area_cache")
def clear_area_cache(sender, instance, **kwargs):
    for key in instance.caches:
        cache.delete(instance.caches[key].format(id=instance.id))
