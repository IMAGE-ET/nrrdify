#!/usr/bin/env python

# ========================================================================
#  Copyright Het Nederlands Kanker Instituut - Antoni van Leeuwenhoek
#
#  Licensed under the 3-clause BSD License
# ========================================================================

import argparse
import logging
import os

import nrrdify


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("inputFolder", metavar="In", type=str, help="Folder containing the DICOM file(s) to convert.")
  parser.add_argument("--out", "-o", help="Folder to store converted files in. If omitted, stores "
                                          "files in parent directory of In folder.")
  parser.add_argument("--name", "-n", help="Filename for the new file, without extension. If omitted, or more series "
                                           "are found, Filename is generated from DICOM tags: "
                                           "<PatientName>-<StudyDate>-<SeriesNumber>. <SeriesDescription>")
  parser.add_argument("--format", "-f", nargs="?", default="nrrd", choices=["nrrd", "nii", "nii.gz"],
                      help="Image format to convert to. Default is the 'nrrd' format")
  parser.add_argument('--logging-level', metavar='LEVEL',
                      choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                      default='WARNING', help='Set capture level for logging')
  parser.add_argument('--log-file', metavar='FILE', type=argparse.FileType('w'), default=None,
                      help='File to append logger output to')
  parser.add_argument('--overwrite', action='store_true', help='if this argument is specified, script will overwrite existing files, '
                                                               'otherwise, file write for already existing files is skipped.')
  parser.add_argument('--check', action='store_true', help='if this argument is specified, DICOMS are checked but not converted.')

  args = parser.parse_args()

  # if specified, set up logging to a file
  if args.log_file is not None:
    log_handler = logging.StreamHandler(args.log_file)
    log_formatter = logging.Formatter('[%(asctime)-.19s] %(levelname)-.1s: %(message)s')
    log_handler.setFormatter(log_formatter)
    logLevel = getattr(logging, args.logging_level)
    log_handler.setLevel(logLevel)

    nrrdify.logger.addHandler(log_handler)
    if logLevel < logging.INFO:  # Lower logger level if necessary
      nrrdify.logger.setLevel(logLevel)

  source_folder = args.inputFolder
  destination_folder = args.out
  if destination_folder is None:
    destination_folder = os.path.dirname(source_folder)

  nrrdify.walk_folder(source_folder, destination_folder, args.name, args.format, args.overwrite, just_check=args.check)

if __name__ == '__main__':
  main()