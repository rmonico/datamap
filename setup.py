from setuptools import setup

setup(name='datamap',
      version='0.1',
      description='A CLI personal folder organizer',
      url='https://github.com/rmonico/datamap',
      author='Rafael Monico',
      author_email='rmonico1@gmail.com',
      license='GPL3',
      packages=['datamap'],
      entry_points = {
          'console_scripts': ['datamap=datamap.datamap:main'],
      },
      zip_safe=False)