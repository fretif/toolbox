from setuptools import setup, find_packages

setup (
       name='CoverageProcessing',
       version='0.1',
       packages=find_packages(),

       # Declare your packages' dependencies here, for eg:
       install_requires=['foo>=3','netCDF4>=1.0.7','scipy>=0.16.1'],

       # Fill in these to make your Egg ready for upload to
       # PyPI
       author='Fabien Retif',
       author_email='fabien.retif@zoho.com',

       #summary = 'Just another Python package for the cheese shop',
       url='',
       license='',
       long_description='Long description of the package',

       # could also include long_description, download_url, classifiers, etc.
  
       )