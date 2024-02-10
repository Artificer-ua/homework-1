import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# sys.path.append(os.path.abspath('..'))

project = 'homework_14'
copyright = '2024, Serg'
author = 'Serg'


extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


html_theme = 'nature'
html_static_path = ['_static']
