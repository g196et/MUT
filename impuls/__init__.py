from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.static import static_view
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .security import groupfinder

from .Models import (
    DBSession,
    Base,
)

def main(global_config, **settings):
    config = Configurator(settings=settings)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings,
                          root_factory='impuls.Models.Root')
    config.include('pyramid_jinja2')
    # Security policies
    authn_policy = AuthTktAuthenticationPolicy(
        settings['impuls.secret'], callback=groupfinder,
        hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_route('home', '/')
    config.add_route('songs', '/songs')
    config.add_route('addSong', '/addSong')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_static_view('static', 'impuls:static', cache_max_age=3600) 
    config.add_static_view('deform_static', 'deform:static/')
    config.scan('.views')
    return config.make_wsgi_app()