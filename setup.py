from setuptools import setup, find_packages, Command
import sys, os

class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import sys,subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


version = '0.1'

setup(name='RPi.TC',
      version=version,
      description="model railway control",
      long_description="""\
Control model railway with Raspberry PI""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      cmdclass = {'test':PyTest},
      keywords='model railway raspberry pi',
      author='Stefan',
      author_email='stefan@terminal21.de',
      url='http://www.terminal21.de',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
