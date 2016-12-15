from dcc_jp2_converter import Exiv2CommandBuilder
from dcc_jp2_converter import exic2CommandBuilders
from dcc_jp2_converter import ImagemagickCommandBuilder
from dcc_jp2_converter import imagemagickCommandBuilders


def main():
    command_builder = ImagemagickCommandBuilder(imagemagickCommandBuilders.Jp2AccessCommandBuilder())


if __name__ == '__main__':
    main()
