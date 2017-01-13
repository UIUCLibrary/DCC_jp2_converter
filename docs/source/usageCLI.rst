Running the Command Line Script
-------------------------------

To convert all the tiff images in the access folders, follow these steps.

1) Open a command prompt/terminal.
2) Type :command:`makejp2` followed by the directory of the collection to convert.

You are done.

For example:

    :command:`makejp2 /Users/hborcher/Documents/dummy`

It's that simple!

The Help Screen
---------------
This documentation should be up to date. However, you can always type :command:`makejp2 -h` into
a command prompt to display the script usage instructions along with any additional the options.

:command:`makejp2 -h`

.. code:: Shell


    usage: makejp2 usage: cli_convert.py [path]

    Create JP2 files from tiffs for digital Library

    positional arguments:
      path               Path to the submission package

    optional arguments:
      -h, --help         show this help message and exit
      --overwrite        Overwrite any existing jp2 with new ones
      --logname LOGNAME  Change the log name.
      --debug            Run script in debug mode`

