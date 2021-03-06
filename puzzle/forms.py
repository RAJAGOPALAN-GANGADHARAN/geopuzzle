from typing import Dict

from django import forms
from django.utils.translation import get_language

from maps.forms import RegionForm


class RegionContainsForm(forms.Form):
    north = forms.FloatField()
    east = forms.FloatField()
    south = forms.FloatField()
    west = forms.FloatField()

    def __init__(self, region, zoom, *args, **kwargs):
        self.region = region
        self.zoom = zoom
        super(RegionContainsForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RegionContainsForm, self).clean()
        data = {part: cleaned_data[part] for part in ['north', 'south', 'west', 'east']}
        diff = (-1, -1, 1, 1)
        extent = self.region.polygon_bounds
        scale = 1.0 / (self.zoom - 2)
        points = [extent[i] + diff[i] * scale for i in range(4)]
        if not (data['north'] < points[3] and data['south'] > points[1] and
                        data['east'] < points[2] and data['west'] > points[0]):
            raise forms.ValidationError('Point not in polygons')


class PuzzleForm(RegionForm):
    def json(self) -> Dict:
        qs = self.regions.filter(id__in=self.game.puzzleregion_set.filter(is_solved=False).
                                 values_list('region_id', flat=True))
        questions = [{
            'id': region.id,
            'name': region.translation.name,
            'polygon': region.polygon_strip,
            'center': region.polygon_center,
            'default_position': self.game.pop_position()}
            for region in qs]
        qs = self.regions.filter(id__in=self.game.puzzleregion_set.filter(is_solved=True).
                                 values_list('region_id', flat=True))
        solved = [region.full_info(get_language()) for region in qs]
        return {'questions': questions, 'solved': solved}
