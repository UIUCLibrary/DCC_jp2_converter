import os

from .utils import logger
from .file_manager import get_tiffs
from tempfile import TemporaryDirectory
import shutil
from .command_runner import CommandRunner
from dcc_jp2_converter import ImagemagickCommandBuilder, exic2CommandBuilders, Exiv2CommandBuilder


def _cleanup_multiple(real_name, path):
    name, ext = os.path.splitext(os.path.basename(real_name))
    duplicates = []

    # find the duplicates with a given name
    for file in os.scandir(path):
        if os.path.splitext(file.name)[1].lower() != ".jp2":
            continue
        if name in file.name:
            duplicates.append(file.path)

    # TODO: Determine the larger of the two.
    sorted_size = sorted(duplicates, key=lambda file: os.path.getsize(file))
    largest = sorted_size[-1]
    assert os.path.getsize(largest) > os.path.getsize(sorted_size[0])
    os.rename(largest, os.path.join(path, real_name))


def convert_tiff_access_folder(path):
    image_convert_command = ImagemagickCommandBuilder()
    metadata_extractor = Exiv2CommandBuilder(exic2CommandBuilders.ExtractIPTCCommand())
    metadata_injector = Exiv2CommandBuilder(exic2CommandBuilders.InsertIPTCCommand())

    with TemporaryDirectory() as tmp_folder:
        command_runner = CommandRunner()
        for tiff in get_tiffs(path):
            tmp_access_tif = os.path.join(tmp_folder, os.path.basename(tiff))
            tmp_access_jp2 = os.path.splitext(tmp_access_tif)[0] + ".jp2"
            final_access_jp2 = os.path.join(path, os.path.basename(tmp_access_jp2))
            if os.path.exists(final_access_jp2):
                logger.warning("{} already exists. skipping".format(final_access_jp2))
                continue

            logger.info("Converting {}".format(os.path.basename(tiff)))

            logger.debug("Copying \"{}\" to temp folder \"{}\"".format(tiff, path))
            shutil.copy2(tiff, tmp_access_tif)

            logger.debug("Using \"{}\" to create \"{}\"".format(tmp_access_tif, tmp_access_jp2))
            im_command = image_convert_command.build_command(tmp_access_tif, tmp_access_jp2)
            try:
                command_runner.run(im_command)
            except RuntimeError as e:
                logger.fatal(e)
                exit(1)
            finally:
                stdout, stderr = command_runner.get_output()
                if stdout:
                    logger.info(stdout)
                if stderr:
                    logger.warning(stderr)

            # HACK: Clean up from Imagemagick because it seems to have a problem with embedded thumbnails
            _cleanup_multiple(os.path.basename(tmp_access_jp2), tmp_folder)

            # Create sidecar metadata files
            logger.debug("Extracting metadata from \"{}\"".format(tmp_access_tif))
            mde_command = metadata_extractor.build_command(tmp_access_tif)
            try:
                command_runner.run(mde_command)
            except RuntimeError as e:
                logger.fatal(e)
                exit(1)
            finally:
                stdout, stderr = command_runner.get_output()
                if stdout:
                    logger.info(stdout)
                if stderr:
                    logger.warning(stderr)

            # Insert sidecar metadata files into jp2
            logger.debug("Injecting metadata into \"{}\"".format(tmp_access_jp2))
            mdi_command = metadata_injector.build_command(tmp_access_jp2)
            try:
                command_runner.run(mdi_command)
            except RuntimeError as e:
                logger.fatal(e)
                exit(1)
            finally:
                stdout, stderr = command_runner.get_output()
                if stdout:
                    logger.info(stdout)
                if stderr:
                    logger.warning(stderr)

            logger.debug("Moving \"{}\" into \"{}\"".format(tmp_access_jp2, path))
            shutil.move(tmp_access_jp2, final_access_jp2)
