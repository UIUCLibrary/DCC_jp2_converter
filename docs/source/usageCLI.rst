Running the Command Line Script
-------------------------------

To convert all the tiff images in the access folders, follow these steps.

1) Open a command prompt/terminal.
2) Type :command:`makejp2` followed by the directory of the collection to convert.


For example:

    :command:`makejp2 /Users/hborcher/Documents/dummy`

It's that simple!

The script will now generate access jp2 files for every tiff file found inside an access folder.

Additional Script Options
-------------------------

This script has a few optional parameters. Add any additional options to the end of the command after the path.

For example the following command will remove the access tif files after it successfully produces a jpeg2000 file.

.. code:: Shell

    makejp2 /Users/hborcher/Documents/dummy --remove

To see the full list of options, use the help screen, explained below.


The Help Screen
---------------
This documentation should be up to date. However, you can always type :command:`makejp2 -h` into
a command prompt to display the script usage instructions along with any additional the options.

:command:`makejp2 -h`

.. code:: Shell

    usage: makejp2 [path] [options]

    Create JP2 files from tiffs for digital Library

    positional arguments:
      path               Path to the submission package

    optional arguments:
      -h, --help         show this help message and exit
      --version          show program's version number and exit
      --overwrite        Overwrite any existing jp2 with new ones
      --remove           Removes access tiff files after converting them.
      --logname LOGNAME  Change the log name.
      --debug            Run script in debug mode`

