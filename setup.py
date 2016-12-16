from setuptools import setup

setup(
    name='DCC_jp2_converter',
    version='0.0.1a0',
    packages=['dcc_jp2_converter', 'dcc_jp2_converter.exiv2Driver',
              'dcc_jp2_converter.ImagemagickDriver'],
    scripts=['scripts/cli_convert.py'],
    entry_points={
        'console_scripts': ['makejp2=convert:main']
    },
    test_suite="tests",
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    data_files=[
        ('settings', ['settings/settings.ini']),
    ],
    zip_safe=False,
    url='',
    license='',
    author='Henry Borchers',
    author_email='hborcher@illinois.edu',
    description='DCC tool for building JP2 access files from Tiff files'
)
