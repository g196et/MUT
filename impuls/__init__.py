from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.static import static_view

from .Base import (
    Base,
)

def main(global_config, **settings):
    config = Configurator(settings=settings)
    engine = engine_from_config(settings, 'sqlalchemy.')
    from sqlalchemy.orm import Session
    session = Session(bind=engine)
    Base.metadata.bind = engine
    config.include('pyramid_jinja2')
    config.add_route('home', '/')
    config.add_route('songs', '/songs')
    #config.add_static_view(name='/static/', path='impuls:static')
    config.add_static_view('static', 'impuls:static', cache_max_age=3600)
    #config.add_static_view('img', path='/static/img')
    #config.add_static_view(name='/static/img/', path='static:img') 
    #config.add_static_view(name='/static/img/photos/', path='static:img:photos')  
    #config.add_static_view(name='/static/img/dirwork/', path='static:img:dirwork')  
    config.scan('.views')
    return config.make_wsgi_app()