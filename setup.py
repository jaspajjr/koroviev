try:
    from setuptools import setup
except ImportError as e:
    from distutils.core import setup

config = {
    'description': 'None of your business',
    'author': 'John Carney',
    'version': '0.1',
    'install_requires': ['pytest', 'pandas', 'numpy', 'scipy']
}

setup(**config)
