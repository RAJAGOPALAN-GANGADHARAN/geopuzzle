from django.conf import settings
from django.utils.translation import ugettext as _

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import BaseUpdateView

from maps.forms import RegionForm
from puzzle.models import Puzzle


@never_cache  # for HTTP headers
def questions(request: WSGIRequest, name: str) -> JsonResponse:
    request._cache_update_cache = False  # disable internal cache
    puzzle = get_object_or_404(Puzzle, slug=name)
    form = RegionForm(data=request.GET, game=puzzle)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)
    result = [{
        'id': region.id,
        'name': region.translation.name,
        'polygon': region.polygon_strip,
        'center': region.polygon_center,
        'default_position': puzzle.pop_position()}
            for region in form.regions]
    return JsonResponse(result, safe=False)


def puzzle(request: WSGIRequest, name: str) -> HttpResponse:
    puzzle = get_object_or_404(Puzzle, slug=name)
    trans = puzzle.load_translation(request.LANGUAGE_CODE)
    context = {
        'google_key': settings.GOOGLE_KEY,
        'language': request.LANGUAGE_CODE,
        'game': puzzle,
        'name': trans.name,
        'text': _('{} was assembled! You time is ').format(trans.name if puzzle.id != 1 else _('World map'))
    }
    return render(request, 'puzzle/map.html', context=context)


class PuzzleEditView(TemplateResponseMixin, BaseUpdateView):
    model = Puzzle
    fields = ['slug']
    queryset = None
    slug_field = 'slug'
    context_object_name = None
    slug_url_kwarg = 'name'
    query_pk_and_slug = False
    template_name = 'puzzle/edit.html'

    def get_context_data(self, **kwargs):
        result = super(PuzzleEditView, self).get_context_data(**kwargs)
        result['countries'] = [{'id': '1', 'name': 'Uganda', 'items': [{'id': '2', 'name': 'Uganda 1'}, {'id': '3', 'name': 'Uganda 2'}]}]
        return result
