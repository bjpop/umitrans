[![travis](https://travis-ci.org/GITHUB_USERNAME/umitrans.svg?branch=master)](https://travis-ci.org/GITHUB_USERNAME/umitrans)

# Overview 

In the examples below, `$` indicates the command line prompt.

# Licence

This program is released as open source software under the terms of [BSD-3-Clause License](https://raw.githubusercontent.com/GITHUB_USERNAME/umitrans/master/LICENSE).

# Installing

You can install umitrans directly from the source code or build and run it from within Docker container.

## Installing directly from source code

Clone this repository: 
```
$ git clone https://github.com/GITHUB_USERNAME/umitrans
```

Move into the repository directory:
```
$ cd umitrans
```

Python 3 is required for this software.

Umitrans can be installed using `pip` in a variety of ways (`$` indicates the command line prompt):

1. Inside a virtual environment:
```
$ python3 -m venv umitrans_dev
$ source umitrans_dev/bin/activate
$ pip install -U /path/to/umitrans
```
2. Into the global package database for all users:
```
$ pip install -U /path/to/umitrans
```
3. Into the user package database (for the current user only):
```
$ pip install -U --user /path/to/umitrans
```


## Building the Docker container 

The file `Dockerfile` contains instructions for building a Docker container for umitrans.

If you have Docker installed on your computer you can build the container like so:
```
$ docker build -t umitrans .
```
See below for information about running umitrans within the Docker container.

# General behaviour

## Help message

Umitrans can display usage information on the command line via the `-h` or `--help` argument:

```
$ umitrans -h
```

## Logging

If the ``--log FILE`` command line argument is specified, umitrans will output a log file containing information about program progress. The log file includes the command line used to execute the program, and a note indicating which files have been processes so far. Events in the log file are annotated with their date and time of occurrence. 

## Exit status values

Umitrans returns the following exit status values:

* 0: The program completed successfully.
* 1: File I/O error. This can occur if at least one of the input FASTA files cannot be opened for reading. This can occur because the file does not exist at the specified path, or umitrans does not have permission to read from the file. 
* 2: A command line error occurred. This can happen if the user specifies an incorrect command line argument. In this circumstance umitrans will also print a usage message to the standard error device (stderr).

# Running within the Docker container

The following section describes how to run umitrans within the Docker container. It assumes you have Docker installed on your computer and have built the container as described above. 
The container behaves in the same way as the normal version of umitrans, however there are some Docker-specific details that you must be aware of.

The general syntax for running umitrans within Docker is as follows:
```
$ docker run -i umitrans CMD
```
where CMD should be replaced by the specific command line invocation of umitrans. Specific examples are below.

Display the help message:
```
$ docker run -i umitrans umitrans -h
```
Note: it may seem strange that `umitrans` is mentioned twice in the command. The first instance is the name of the Docker container and the second instance is the name of the umitrans executable that you want to run inside the container.

Display the version number:
```
$ docker run -i umitrans umitrans --version
```

# Bug reporting and feature requests

Please submit bug reports and feature requests to the issue tracker on GitHub:

[umitrans issue tracker](https://github.com/bjpop/umitrans/issues)
