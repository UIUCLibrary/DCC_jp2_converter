"""DCC_jp2_converter.

Script to create JP2 access images with embedded metadata from tiff access
masters to be used by the Digital Library.

"""
import os
from setuptools import setup
from shared_setup import metadata

setup(**metadata,
      entry_points={
          'console_scripts': ['makejp2=dcc_jp2_converter.scripts.cli:main']
      },
      package_data={
          'dcc_jp2_converter.thirdparty': ['*'],
      },
      include_package_data=True,
      test_suite="tests",
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      data_files=[
          ('settings', ['settings/command_paths.ini']),
          (os.path.expanduser("~"), ['settings/command_paths.ini']),
      ],
      zip_safe=False,

      )
