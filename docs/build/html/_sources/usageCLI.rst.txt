This is a command line script so you will need a terminal window open to use it.


Create access jp2 files from access tiffs
-----------------------------------------

To convert all the tiff images in the access folders, type :command:`makejp2` followed by the directory of the
collection to convert.


For example:

    :command:`makejp2 /Users/hborcher/Documents/dummyCollection`

The script will now generate access jp2 files for every tiff file found inside an access folder.

Clean up extra files after converting
-------------------------------------

After you've created all your access jp2 files from the access tiffs, you might want to remove the extra access tiffs.
To do this, you can clean up this folder using the :command:`--clean` option flag.

This option will look for access folders for matching jp2 and tiff files. It it finds a match, it will delete the
access tiff but leave the jp2.


For example:

    :command:`makejp2 /Users/hborcher/Documents/dummyCollection --clean`

.. note::

    Any files not in a folder named "access" will be ignored.


Delete files automatically after converting
-------------------------------------------

You can also combine these steps so that the script automatically delete the access tiff file after it successfully
generates a jp2 file. To do this, you can use the :command:`--remove` option flag.

For example:

    :command:`makejp2 /Users/hborcher/Documents/dummyCollection --remove`


The Help Screen
---------------
This documentation should be up to date. However, you can always type :command:`makejp2 -h` into
a command prompt to display the script usage instructions along with any additional the options.

:command:`makejp2 -h`

.. code-block:: console

    usage: makejp2 [path] [options]

    Create JP2 files from tiffs for digital Library

    positional arguments:
      path               Path to the submission package

    optional arguments:
      -h, --help         show this help message and exit
      --version          show program's version number and exit
      --overwrite        Overwrite any existing jp2 with new ones
      --clean            Clean up folders by removing any access tiff that have
                         already been converted into jp2
      --remove           Removes access tiff files after converting them.
      --logname LOGNAME  Change the log name.
      --debug            Run script in debug mode


It's that simple!