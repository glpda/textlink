#!/usr/bin/env python3

import argparse
import configparser
# import os
import re


class UnsupportedFileFormat(Exception):
    pass

class InvalidDesktopEntryType(Exception):
    pass


class TextLink:
    def __init__(self, url):
        if type(url) == str:
            self.url = url
        else:
            raise TypeError

    def __str__(self):
        return self.url

    def __eq__(self, other):
        return self.url == other.url

    def toTextLink(self):
        return TextLink(self.url)

    def toWindowsURL(self):
        return WindowsURL(self.url)

    def toFreeDesktop(self, name):
        return FreeDesktop(self.url, name)


class FreeDesktop(TextLink):
    icon = "text-html"
    def __init__(self, url, name):
        super().__init__(url)
        self.name = name

    def __str__(self):
        return "[Desktop Entry]\n"\
               "Type=Link\n"\
               "Icon=" + self.icon + "\n"\
               "Name=" + self.name + "\n"\
               "URL="  + self.url  + "\n"

    def __eq__(self, other):
        return self.icon == other.icon \
           and self.name == other.name \
           and self.url  == other.url

    def read_string(string):
        ini = configparser.ConfigParser()
        ini.read_string(string)
        if ini['Desktop Entry']['Type'] != "Link":
            raise InvalidDesktopEntryType
        url = ini['Desktop Entry']['URL']
        name = ini['Desktop Entry']['Name']
        return FreeDesktop(url, name)

    def read_file(f):
        ini = configparser.ConfigParser()
        ini.read_file(f)
        if ini['Desktop Entry']['Type'] != "Link":
            raise InvalidDesktopEntryType
        url = ini['Desktop Entry']['URL']
        name = ini['Desktop Entry']['Name']
        return FreeDesktop(url, name)

    def toFreeDesktop(self):
        return FreeDesktop(self.url, self.name)


class WindowsURL(TextLink):
    def __str__(self):
        return "[InternetShortcut]\n"\
               "IconFile=C:\\WINDOWS\\SYSTEM\\url.dll\n"\
               "IconIndex=1\n"\
               "URL=" + self.url + "\n"

    def read_string(string):
        ini = configparser.ConfigParser()
        ini.read_string(string)
        url = ini['InternetShortcut']['URL']
        return WindowsURL(url)

    def read_file(f):
        ini = configparser.ConfigParser()
        ini.read_file(f)
        url = ini['InternetShortcut']['URL']
        return WindowsURL(url)


def main():
    parser = argparse.ArgumentParser(
                        prog = "textlink",
                        description="convert textual link file formats (.url, .desktop)",
                        epilog="deduce file formats from file extension")
    parser.add_argument("input", help="input file name")
    parser.add_argument("output", help="output file name")
    args = parser.parse_args()

    pattern = re.compile(r"(.*)\.(.+)$")
    input_extension = pattern.match(args.input).group(2)
    output_name, output_extension = pattern.match(args.output).group(1, 2)

    if input_extension == "desktop":
        with open(args.input, "r") as f:
            input_link = FreeDesktop.read_file(f)
    elif input_extension == "url":
        with open(args.input, "r") as f:
            input_link = WindowsURL.read_file(f)
    else:
        raise UnsupportedFileFormat

    if output_extension == "desktop":
        output_link = input_link.toFreeDesktop(output_name)
    elif output_extension == "url":
        output_link = input_link.toWindowsURL()
    else:
        raise UnsupportedFileFormat

    with open(args.output, "w") as f:
        f.write(str(output_link))



if __name__ == '__main__':
    main()
