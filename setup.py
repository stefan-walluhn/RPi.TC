from setuptools import setup, find_packages


version = '0.1'

setup(name='RPi.TC',
      version=version,
      description="model railway control",
      long_description="""\
Control model railway with Raspberry PI""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='model railway raspberry pi',
      author='Stefan',
      author_email='stefan@terminal21.de',
      url='http://www.terminal21.de',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "Click",
          "RPi.GPIO",
          "future",
          "fysom",
          "mock",
          "pika",
          "protobuf",
          "pytest-runner",
          "pyyaml",
      ],
      tests_require=[
          "pytest",
          "pytest-datadir",
          "pytest-flake8",
      ],
      entry_points={
          'console_scripts': [
              'rptc_listener = rpitc.cli.listener:listen',
              'rptc_request_trail = rpitc.cli.request:trail',
          ],
      },
)
