Configure
---------

Since this script works by sending commands to external command line programs, the location of these external
programs must be know to the script.

These programs are:

- Imagemagick 6 (NOT version 7+)

- exiv2

Without any configuration, the script will default to searching on the path for these programs. However if these
programs are not found on the path or alternative version of these programs are desired a command_paths.ini
configuration file must be created.

A command_paths.ini found in the home directory will override any default settings.

command_paths.ini format
''''''''''''''''''''''''

The command_paths.ini contains:

- one section: [commands]

- 2 optional keys: convert and exiv2

=======   =============================
 Key       Value
=======   =============================
convert   Imagemagick 6 convert command
exiv2     exiv2 command
=======   =============================


A example of this file would look like this::

    [commands]
    convert = C:\Users\hborcher\Downloads\ImageMagick-6.9.7-3-portable-Q16-x86\convert.exe
    exiv2 = C:\Users\hborcher\Downloads\exiv2-0.25-win\exiv2.exe

