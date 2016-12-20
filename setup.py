import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()

requires = [
    'pyramid',
    'pyramid_jinja2',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'bcrypt',
    'deform',
]

setup(name='impuls',
      install_requires=requires,
      version='0.0',
      description='impuls',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Studio MUT',
      author_email='',
      url='ssoimpuls.ru',
      keywords='web wsgi bfg pylons pyramid',
      test_suite='impuls',
      entry_points="""\
      [paste.app_factory]
      main = impuls:main
      [console_scripts]
      initialize_impuls_db = impuls.scripts.initDB:main
      """,
)