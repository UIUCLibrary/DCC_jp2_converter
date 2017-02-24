Configure
---------

Since this script works by sending commands to external command line programs, the location of these external
programs must be known to the script.

These programs are:

- Imagemagick 6 (NOT version 7+)

- exiv2

Without any configuration, the script will default to searching on the path for these programs. However if these
programs are not found on the path or alternative version of these programs are desired a command_paths.ini
configuration file must be created.

A command_paths.ini found in the home directory will override any default settings.


.. admonition:: TL;DR

    - If Imagemagick 6 & exiv2 are on installed on the path, no configuration is necessary.

    - To specify specific paths for these programs, create a command_paths.ini in your home directory.

.. note::
    Windows has a system level program called convert.exe, located in C:\\Windows\\System32\. This is for converting the
    filesystem of a hard drive. **THIS IS NOT Imagemagick**. Do not configure the command_paths.ini settings files to use
    this program. It will not work.

.. warning::

    Only Imagemagick 6 will currently work. Imagemagick 7 made changes to the command and won't work.


command_paths.ini format
''''''''''''''''''''''''

The command_paths.ini contains:

- one section: [commands]

- 2 optional keys: convert and exiv2

=======   ==============================  ==============
 Key       Value                           Windows Name
=======   ==============================  ==============
convert   Imagemagick 6 convert command.  convert.exe
exiv2     exiv2 command                   exiv2.exe
=======   ==============================  ==============


A example of this file on Windows would look like this::

    [commands]
    convert = C:\Users\hborcher\Downloads\ImageMagick-6.9.7-3-portable-Q16-x86\convert.exe
    exiv2 = C:\Users\hborcher\Downloads\exiv2-0.25-win\exiv2.exe

