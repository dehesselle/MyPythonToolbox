# SPDX-License-Identifier: MIT
# https://github.com/dehesselle/MyPythonToolbox

# usage:
#
#   ini = IniFile.IniFile("test.ini")
#   ini["mysection"] = {}
#   ini["mysection"]["mykey"] = "myvalue"

import configparser
import os
import errno
import pathlib
from touch import touch
import atexit


class IniFile:
    def __init__(self, filename="", create=True):
        if not filename:
            raise ValueError("filename required")

        self.filename = os.path.basename(filename)
        self.directory = os.path.dirname(filename)

        if not self.directory:
            self.directory = os.getenv("XDG_CONFIG_HOME")

        # prefer XDG_CONFIG_HOME over HOME
        if self.directory:
            # create if not exists
            if not os.path.isdir(self.directory):
                os.makedirs(self.directory)
        else:
            # last resort: use HOME
            self.directory = str(pathlib.Path.home())

        self.configParser = configparser.ConfigParser()

        ini_file = self.directory + "/" + self.filename
        if not os.path.exists(ini_file):
            if create:
                touch(ini_file)
            else:
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), ini_file)

        self.configParser.read(ini_file)
        atexit.register(self.save)  # save ini

    def save(self):
        try:
            ini_file = self.directory + "/" + self.filename
            with open(ini_file, "w") as config:
                self.configParser.write(config)
        except OSError as e:
            print("unable to save:", ini_file)

    def __getitem__(self, item):
        return self.configParser[item]

    def __contains__(self, key):
        return self.configParser.__contains__(key)

    def __setitem__(self, item1, item2="", item3=""):
        if not item3:
            self.configParser[item1] = item2
        else:
            self.configParser[item1][item2] = item3
