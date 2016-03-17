from setuptools import setup, find_packages

setup (
       name='timeseries-processing',
       version='0.1',
       packages=find_packages(),

       # Declare your packages' dependencies here, for eg:
       install_requires=['pandas>=0.17.1'],

       author='Fabien Retif',
       author_email='fabien.retif@zoho.com',

       #summary = 'Just another Python package for the cheese shop',
       url='',
       license='',
       long_description='Toolbox for processing timeseries (extract, convert)',

       # could also include long_description, download_url, classifiers, etc.

  
       )