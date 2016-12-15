from setuptools import setup

setup(
    name='DCC_jp2_converter',
    version='0.0.1a0',
    packages=['exiv2Driver', 'ImagemagickDriver'],
    scripts=['scripts/convert.py'],
    test_suite="tests",
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
