"""DCC_jp2_converter.

Script to create JP2 access images with embedded metadata from tiff access
masters to be used by the Digital Library.

"""
import os
from setuptools import setup
import dcc_jp2_converter

metadata = {
    # "name": 'DCC_jp2_converter',
    "packages": ['dcc_jp2_converter',
                 'dcc_jp2_converter.modules',
                 'dcc_jp2_converter.modules.profiles',
                 'dcc_jp2_converter.modules.exiv2Driver',
                 'dcc_jp2_converter.modules.exiv2Driver.exiv2CommandBuilders',
                 'dcc_jp2_converter.modules.imagemagick_driver',
                 'dcc_jp2_converter.modules.imagemagick_driver.imagemagick_command_builders',
                 'dcc_jp2_converter.modules.kakaduDriver',
                 'dcc_jp2_converter.scripts',
                 'dcc_jp2_converter.thirdparty'
                 ],

    "license": '',


}

setup(**metadata,
      name=dcc_jp2_converter.__title__,
      description=dcc_jp2_converter.__description__,
      entry_points={
          'console_scripts': ['makejp2=dcc_jp2_converter.scripts.cli:main']
      },
      version=dcc_jp2_converter.__version__,
      author=dcc_jp2_converter.__author__,
      author_email=dcc_jp2_converter.__author_email__,
      url=dcc_jp2_converter.__url__,
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
