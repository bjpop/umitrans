'''
Module      : Main
Description : The main entry point for the program.
Copyright   : (c) Bernie Pope, 22 Dec 2020 
License     : BSD-3-Clause 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

from argparse import ArgumentParser
import sys
import logging
import pkg_resources
from itertools import zip_longest, islice
from contextlib import ExitStack
import pyfastx 


EXIT_FILE_IO_ERROR = 1
EXIT_COMMAND_LINE_ERROR = 2
PROGRAM_NAME = "umitrans"
DEFAULT_SEPARATOR = ":"

# We assume that FASTQ files are formatted to 4 lines per record, where
# the 
START_LINE = 2
STEP_SIZE = 4

try:
    PROGRAM_VERSION = pkg_resources.require(PROGRAM_NAME)[0].version
except pkg_resources.DistributionNotFound:
    PROGRAM_VERSION = "undefined_version"


def exit_with_error(message, exit_status):
    '''Print an error message to stderr, prefixed by the program name and 'ERROR'.
    Then exit program with supplied exit status.

    Arguments:
        message: an error message as a string.
        exit_status: a positive integer representing the exit status of the
            program.
    '''
    logging.error(message)
    print("{} ERROR: {}, exiting".format(PROGRAM_NAME, message), file=sys.stderr)
    sys.exit(exit_status)


def parse_args():
    '''Parse command line arguments.
    Returns Options object with command line argument values as attributes.
    Will exit the program on a command line error.
    '''
    description = 'Transfer UMI sequences from a FASTQ file to read IDs in one or more FASTQ files'
    parser = ArgumentParser(description=description)
    parser.add_argument('--version', action='version', version='%(prog)s ' + PROGRAM_VERSION)
    parser.add_argument('--log', metavar='LOG_FILE', type=str, help='record program progress in LOG_FILE')
    parser.add_argument('--umi', metavar='FILE', type=str, required=True, help='FASTQ file containing UMI sequences')
    parser.add_argument('--sep', metavar='STR', type=str, default=DEFAULT_SEPARATOR, help='Separator between read ID and UMI, default is \'%(default)s\'')
    parser.add_argument('--seq', nargs='+', metavar='FILE', type=str, help='Input FASTQ files')
    return parser.parse_args()


def init_logging(log_filename):
    '''If the log_filename is defined, then
    initialise the logging facility, and write log statement
    indicating the program has started, and also write out the
    command line from sys.argv

    Arguments:
        log_filename: either None, if logging is not required, or the
            string name of the log file to write to
    Result:
        None
    '''
    if log_filename is not None:
        logging.basicConfig(filename=log_filename,
                            level=logging.DEBUG,
                            filemode='w',
                            format='%(asctime)s %(levelname)s - %(message)s',
                            datefmt="%Y-%m-%dT%H:%M:%S%z")
        logging.info('program started')
        logging.info('command line: %s', ' '.join(sys.argv))

def process_files(options):
    input_filenames = [options.umi] + options.seq
    input_files = [pyfastx.Fastx(fname) for fname in input_filenames] 
    output_filenames = [name + ".umi" for name in options.seq]
    output_files = [open(fname, "w") for fname in output_filenames]
    for records in zip_longest(*input_files):
        if len(records) >= 1:
           umi_record = records[0]
           if umi_record is not None and len(umi_record) == 4:
               umi_name, umi_seq, _umi_qual, umi_comment = umi_record
           else:
               exit_with_error(f"Badly formed UMI record in input UMI FASTQ file: {umi_record}", EXIT_FILE_IO_ERROR)
           fastq_records = records[1:]
           for output_file, this_record in zip(output_files, fastq_records):
               if this_record is not None and len(this_record) == 4:
                   this_name, this_seq, this_qual, this_comment = this_record 
                   if this_name == umi_name:
                       new_name = this_name + options.sep + umi_seq
                       print(f"@{new_name} {this_comment}\n{this_seq}\n+\n{this_qual}", file=output_file)
               else:
                   exit_with_error(f"Badly formed FASTQ record in input FASTQ file: {this_record}", EXIT_FILE_IO_ERROR)
    # FASTX does not appear to provide a proper context manager for files, so
    # we resort to trying to close files here.
    for file in input_files:
        file.close()
    for file in output_files:
        file.close()
      

def main():
    "Orchestrate the execution of the program"
    options = parse_args()
    init_logging(options.log)
    process_files(options)


# If this script is run from the command line then call the main function.
if __name__ == '__main__':
    main()
