from setuptools import setup

setup(name='PySOS Web',
      version='.1',
      description='Web based helper for the pysos utility',
      author='Wallace Daniel',
      author_email='wdaniel@redhat.com',
      url='pysosweb-wdaniel.itos.redhat.com',
      install_requires=['Flask>=0.7.2', 'MarkupSafe','Flask-SQLAlchemy'],
     )
