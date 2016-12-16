from pyramid.view import (
    view_config,
    view_defaults
    )
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound


@view_defaults(renderer='templates/home.jinja2')
class MyViews:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='home', renderer = 'templates/index.jinja2')
    def home(self):
        return {'name': '"ССО Импульс"'}

    @view_config(route_name='songs', renderer = 'templates/songs.jinja2')
    def songs(self):
        return {'name': 'Вторая страница'}