"""High-level logic for orchestrating a conversion job."""

import abc
import logging
import os
import stat
import shutil
import tempfile
from .file_manager import get_tiffs
from .command_runner import CommandRunner
from dcc_jp2_converter import ImagemagickCommandBuilder, Exiv2CommandBuilder, KakaduCommandBuilder
from dcc_jp2_converter import imagemagickCommandBuilders as im_cb
from dcc_jp2_converter import kakaduCommandBuilders as kd_cb
from dcc_jp2_converter import exiv2CommandBuilders as exi2_cb

logger = logging.getLogger("dcc_jp2_converter")


class Converter(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def convert_tiff_access_folder(path: str, overwrite_existing=True, remove_on_success=False):
        pass

    @staticmethod
    def create(name):
        CONVERTERS = {
            "ImageMagick": ImageMagickConverter,
            "Kakadu": KakaduConverter
        }

        try:
            return CONVERTERS[name]
        except KeyError:
            raise AttributeError("Invalid converter {}".format(name))


class ImageMagickConverter(Converter):
    @staticmethod
    def convert_tiff_access_folder(path: str, overwrite_existing=True, remove_on_success=False):
        convert_tiff_access_folder(path, overwrite_existing, remove_on_success)


class KakaduConverter(Converter):
    @staticmethod
    def convert_tiff_access_folder(path: str, overwrite_existing=True, remove_on_success=False):
        total_files_converted = 0
        image_convert_command = KakaduCommandBuilder(builder=kd_cb.HathiPreset())
        with tempfile.TemporaryDirectory(prefix="convert_") as tmp_folder:
            print()
            command_runner = CommandRunner()
            tiffs = list(get_tiffs(path))
            for i, tiff in enumerate(tiffs):
                tmp_access_tif = os.path.join(tmp_folder, os.path.basename(tiff))
                tmp_access_jp2 = os.path.splitext(tmp_access_tif)[0] + ".jp2"
                final_access_jp2 = os.path.join(
                    path, os.path.basename(tmp_access_jp2))

                if not overwrite_existing:
                    if os.path.exists(final_access_jp2):
                        logger.warning(
                            "{} already exists. skipping".format(final_access_jp2))
                        continue

                logger.info("Converting part {} of {}: From {} to {} ".format(
                    i + 1, len(tiffs), os.path.basename(tiff),
                    os.path.basename(final_access_jp2)))

                logger.debug(
                    "Copying \"{}\" to temp folder \"{}\"".format(tiff, path))

                shutil.copyfile(tiff, tmp_access_tif)

                logger.debug(
                    "Using \"{}\" to create \"{}\"".format(
                        tmp_access_tif, tmp_access_jp2))

                im_command = image_convert_command.build_command(
                    tmp_access_tif, tmp_access_jp2)

                try:

                    command_runner.run(im_command)
                    if remove_on_success:
                        logger.info("Deleting file, \"{}\".".format(tiff))
                        os.remove(tiff)

                except RuntimeError as e:
                    logger.error(e)
                    raise
                finally:
                    pass
                    stdout, stderr = command_runner.get_output()
                    if stdout:
                        logger.info(stdout)
                    if stderr:
                        logger.warning(stderr)
                logger.debug("Moving \"{}\" into \"{}\"".format(tmp_access_jp2, path))
                shutil.move(tmp_access_jp2, final_access_jp2)
                total_files_converted += 1
            logger.info("Converted {} file(s) in {}.".format(total_files_converted, path))

            # raise NotImplementedError


def _cleanup_multiple(real_name, path):
    """
    This is a hack that I had to write because imagemagick makes multiple
    files when it finds an embedded thumbnail in the tiff file. This function
    looks for any files that contain the "real name" in it and renames the
    largest one to that name it was supposed to have from the start.

    Args:
        real_name: the name of the file it supposed to be saved as
        path: the path were the multiple version of the file are stored.

    """
    name, ext = os.path.splitext(os.path.basename(real_name))
    duplicates = []

    # find the duplicates with a given name
    for file in os.scandir(path):
        if os.path.splitext(file.name)[1].lower() != ".jp2":
            continue
        if name in file.name:
            duplicates.append(file.path)

    sorted_size = sorted(duplicates, key=lambda f: os.path.getsize(f))
    largest = sorted_size[-1]
    assert os.path.getsize(largest) >= os.path.getsize(sorted_size[0])
    os.rename(largest, os.path.join(path, real_name))


def convert_tiff_access_folder(path: str, overwrite_existing=True, remove_on_success=False):
    """
    Converts all tiff files located in that folder into JP2000 .jp2 files and
    migrated all the metadata from the tiff file into the newly produced jp2
    file. All new files are saved in the same place that as their source files.

    Args:
        path: The path to the folder containing tiff files to be converter.
        overwrite_existing: If an existing jp2 file already exists in the same
         folder, overwrite it with a new file.
        remove_on_success: Delete access tiff file afterwards if successfully converted.


    """
    image_convert_command = ImagemagickCommandBuilder(builder=im_cb.Standard())
    metadata_extractor = Exiv2CommandBuilder(exi2_cb.ExtractIPTCCommand())
    metadata_injector = Exiv2CommandBuilder(exi2_cb.InsertIPTCCommand())

    with tempfile.TemporaryDirectory(prefix="convert_") as tmp_folder:
        command_runner = CommandRunner()
        tiffs = list(get_tiffs(path))
        total_files_converted = 0

        for i, tiff in enumerate(tiffs):
            tmp_access_tif = os.path.join(tmp_folder, os.path.basename(tiff))
            tmp_access_jp2 = os.path.splitext(tmp_access_tif)[0] + ".jp2"
            final_access_jp2 = os.path.join(
                path, os.path.basename(tmp_access_jp2))

            if not overwrite_existing:
                if os.path.exists(final_access_jp2):
                    logger.warning(
                        "{} already exists. skipping".format(final_access_jp2))
                    continue

            logger.info("Converting part {} of {}: From {} to {} ".format(
                i + 1, len(tiffs), os.path.basename(tiff),
                os.path.basename(final_access_jp2)))

            logger.debug(
                "Copying \"{}\" to temp folder \"{}\"".format(tiff, path))

            shutil.copyfile(tiff, tmp_access_tif)

            logger.debug(
                "Using \"{}\" to create \"{}\"".format(
                    tmp_access_tif, tmp_access_jp2))

            im_command = image_convert_command.build_command(
                tmp_access_tif, tmp_access_jp2)

            try:

                command_runner.run(im_command)
                if remove_on_success:
                    # remove the read only attribute first
                    os.chmod(tiff, stat.S_IWRITE)

                    logger.info("Deleting file, \"{}\".".format(tiff))
                    os.remove(tiff)

            except RuntimeError as e:
                logger.error(e)
                raise
                # exit(1)
            finally:
                stdout, stderr = command_runner.get_output()
                if stdout:
                    logger.info(stdout)
                if stderr:
                    logger.warning(stderr)

            # HACK: Clean up from Imagemagick because it seems to have a
            # problem with embedded thumbnails
            _cleanup_multiple(os.path.basename(tmp_access_jp2), tmp_folder)

            # Create sidecar metadata files
            logger.debug(
                "Extracting metadata from \"{}\"".format(tmp_access_tif))

            mde_command = metadata_extractor.build_command(tmp_access_tif)
            try:
                command_runner.run(mde_command)

            except RuntimeError as e:
                logger.error(e)
                exit(1)
            finally:
                stdout, stderr = command_runner.get_output()
                if stdout:
                    logger.info(stdout)
                if stderr:
                    logger.warning(stderr)

            # Insert sidecar metadata files into jp2
            logger.debug(
                "Injecting metadata into \"{}\"".format(tmp_access_jp2))

            mdi_command = metadata_injector.build_command(tmp_access_jp2)
            try:
                command_runner.run(mdi_command)

            except RuntimeError as e:
                logger.error(e)
                exit(1)
            finally:
                stdout, stderr = command_runner.get_output()
                if stdout:
                    logger.info(stdout)
                if stderr:
                    logger.warning(stderr)

            logger.debug("Moving \"{}\" into \"{}\"".format(tmp_access_jp2, path))
            shutil.move(tmp_access_jp2, final_access_jp2)
            total_files_converted += 1
        logger.info("Converted {} file(s) in {}.".format(total_files_converted, path))
