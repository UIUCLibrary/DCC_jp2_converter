from dcc_jp2_converter import __version__ as version

metadata = {
    "name": 'DCC_jp2_converter',
    "version": version,
    "packages": ['dcc_jp2_converter',
                 'dcc_jp2_converter.modules',
                 'dcc_jp2_converter.modules.exiv2Driver',
                 'dcc_jp2_converter.modules.exiv2Driver.exiv2CommandBuilders',
                 'dcc_jp2_converter.modules.ImagemagickDriver',
                 'dcc_jp2_converter.modules.ImagemagickDriver.imagemagickCommandBuilders',
                 'dcc_jp2_converter.modules.kakaduDriver',
                 'dcc_jp2_converter.scripts',
                 'dcc_jp2_converter.thirdparty'
                 ],
    "url": 'https://github.com/UIUCLibrary/DCC_jp2_converter',
    "license": '',
    "author": 'Henry Borchers',
    "author_email": 'hborcher@illinois.edu',
    "description": 'DCC tool for building JP2 access files from Tiff files',

}
