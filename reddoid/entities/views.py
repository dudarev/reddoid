import datetime

from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import decorators
from django.views.decorators import csrf
from django.views.generic.base import TemplateView, View
from django.utils import simplejson

from entities.models import Link, Image


# https://github.com/mitar/django-missing/blob/master/missing/views.py#L7
class EnsureCsrfCookieMixin(object):
    """
    Mixin for Django class-based views which forces a view to send the CSRF cookie.
    """
    @decorators.method_decorator(csrf.ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(EnsureCsrfCookieMixin, self).dispatch(*args, **kwargs)


class AjaxView(View):
    http_method_names = ['get']
    response_class = HttpResponse

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'application/json'
        return self.response_class(simplejson.dumps(context), **response_kwargs)


class LinksHtmlView(TemplateView):
    template_name = 'entities/links_html.html'

    def get(self, request, *args, **kwargs):
        try:
            date = datetime.datetime(
                year=int(kwargs['year']), month=int(kwargs['month']),
                day=int(kwargs['day']))
        except (TypeError, ValueError, KeyError):
            date = datetime.datetime.now()
        return self.render_to_response({
                'date': date,
                'entities_name': 'links',
                'authenticated': request.user.is_authenticated()})


class LinksAjaxView(AjaxView):

    def get(self, request, *args, **kwargs):
        page = request.GET.get('page')
        try:
            date = datetime.datetime.strptime(
                request.GET.get('date'),
                '%Y-%m-%d')
        except (ValueError, TypeError):
            date = datetime.datetime.now()
        paginator = Paginator(
            Link.objects.all().filter(date=date).exclude(title__isnull=True),
            25,
            orphans=10)
        try:
            entities = paginator.page(page)
        except PageNotAnInteger:
            entities = paginator.page(1)
        except EmptyPage:
            entities = []
        links = [{
            'url': e.url,
            'votes': e.votes_count,
            'title': e.title,
        } for e in entities]
        return self.render_to_response({'entities': links})


class ImagesView(TemplateView):
    """docstring for ImagesView"""
    # mode = Image
    template_name = 'entities/image_list.html'

    def get(self, request, *args, **kwargs):
        try:
            date = datetime.datetime(
                year=int(kwargs['year']), month=int(kwargs['month']),
                day=int(kwargs['day']))
        except (TypeError, ValueError, KeyError):
            date = datetime.datetime.now()
        # return date
        # date = datetime.datetime.now()
        return self.render_to_response(
            {
                'date': date,
                'entities_name': 'images',
                'authenticated': request.user.is_authenticated(),
            })


class ImagesAjaxView(AjaxView):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('page')
        try:
            date = datetime.datetime.strptime(
                request.GET.get('date'),
                '%Y-%m-%d')
        except (ValueError, TypeError):
            date = datetime.datetime.now()
        paginator = Paginator(
            Image.objects.all().filter(date=date),
            25,
            orphans=10)
        try:
            entities = paginator.page(page)
        except PageNotAnInteger:
            entities = paginator.page(1)
        except EmptyPage:
            entities = []
        links = [{
            'url': e.url,
            'votes': e.votes_count,
            'title': e.title,
        } for e in entities]
        return self.render_to_response({'entities': links})

