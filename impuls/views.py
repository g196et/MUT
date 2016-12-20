from pyramid.security import (
    remember,
    forget,
    )

from pyramid.view import (
    view_config,
    view_defaults
    )

from .Models import (
    DBSession,
    Base,
    Song,
)

import colander
import deform.widget

from .security import (
    USERS,
    check_password
)

from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound

@view_defaults(renderer='templates/home.jinja2')
class MyViews:
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @view_config(route_name='home', renderer = 'templates/index.jinja2')
    def home(self):
        return {'name': '"ССО Импульс"'}

    @view_config(route_name='songs', renderer = 'templates/songs.jinja2')
    def songs(self):
        request = self.request
        if 'form.submitted' in request.params:
            body = request.params['body']
            title = request.params['title']
            DBSession.add(Song(SongTitle = title, SongText = body, SongWriter = "11"))
        songs = DBSession.query(Song).order_by(Song.idSong)
        return {'songs':songs}

    @view_config(route_name='login', renderer='templates/login.jinja2')
    def login(self):
        request = self.request
        login_url = request.route_url('login')
        referrer = request.url
        if referrer == login_url:
            referrer = '/'  # never use login form itself as came_from
        came_from = request.params.get('came_from', referrer)
        message = ''
        login = ''
        password = ''
        if 'form.submitted' in request.params:
            login = request.params['login']
            password = request.params['password']
            if check_password(password, USERS.get(login)):
                headers = remember(request, login)
                return HTTPFound(location=came_from,
                                 headers=headers)
            message = 'Failed login'

        return {
            'name':'Login',
            'message':message,
            'url':request.application_url + '/login',
            'came_from':came_from,
            'login':login,
            'password':password,
        }

    @view_config(route_name='logout')
    def logout(self):
        request = self.request
        headers = forget(request)
        url = request.route_url('home')
        return HTTPFound(location=url,
                         headers=headers)