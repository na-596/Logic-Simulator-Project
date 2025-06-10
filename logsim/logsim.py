#!/usr/bin/env python3
"""Parse command line options and arguments for the Logic Simulator.

This script parses options and arguments specified on the command line, and
runs either the command line user interface or the graphical user interface.

Usage
-----
Show help: logsim.py -h
Command line user interface: logsim.py -c <file path>
Graphical user interface: logsim.py <file path>
"""
import getopt
import sys

import wx

from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner
from parse import Parser
from userint import UserInterface
from gui import Gui
import os


def main(arg_list):
    """Parse the command line options and arguments specified in arg_list.

    Run either the command line user interface, the graphical user interface,
    or display the usage message.
    """
    usage_message = ("Usage:\n"
                     "Show help: logsim.py -h\n"
                     "Command line user interface: logsim.py -c <file path>\n"
                     "Graphical user interface: logsim.py <file path>")
    try:
        options, arguments = getopt.getopt(arg_list, "hc:")
        print('options:', options, 'arguments:', arguments)
    except getopt.GetoptError:
        print("Error: invalid command line arguments\n")
        print(usage_message)
        sys.exit()

    # Initialise instances of the four inner simulator classes
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    # names = None
    # devices = None
    # network = None
    # monitors = None

    for option, path in options:
        if option == "-h":  # print the usage message
            print(usage_message)
            sys.exit()
        elif option == "-c":  # use the command line user interface
            scanner = Scanner(path, names)
            parser = Parser(names, devices, network, monitors, scanner)
            if parser.parse_network():
                # Initialise an instance of the userint.UserInterface() class
                userint = UserInterface(names, devices, network, monitors)
                userint.command_interface()

    if not options:  # no option given, use the graphical user interface

        if len(arguments) != 1:  # wrong number of arguments
            print("Error: one file path required\n")
            print(usage_message)
            sys.exit()

        [path] = arguments
        scanner = Scanner(path, names)
        parser = Parser(names, devices, network, monitors, scanner)
        if parser.parse_network():
            # get the language from the environment variable LANG
            language = os.getenv('LANG', 'en_GB.UTF-8')
            print("Current LANG:", language)
            # Initialise an instance of the gui.Gui() class
            app = wx.App()
            locale = wx.Locale()
            lang = wx.LANGUAGE_ENGLISH  # Default
            if language in ["es_ES.utf8", "es_ES.UTF-8", "es_ES"]:
                lang = wx.LANGUAGE_SPANISH
            elif language in ["zh_CN.utf8", "zh_CN.UTF-8", "zh_CN"]:
                lang = wx.LANGUAGE_CHINESE_SIMPLIFIED
            elif language in ["ta_IN.utf8", "ta_IN.UTF-8", "ta_IN"]:
                lang = wx.LANGUAGE_TAMIL
            elif language in ["yo_NG.utf8", "yo_NG.UTF-8", "yo_NG"]:
                lang = wx.LANGUAGE_YORUBA
            elif language in ["kn_IN.utf8", "kn_IN.UTF-8", "kn_IN"]:
                lang = wx.LANGUAGE_KANNADA
            # Add more languages as needed

            locale.Init(lang)
            # Set the path to your locale directory
            locale_dir = os.path.join(os.path.dirname(__file__), "locale")
            locale.AddCatalogLookupPathPrefix(locale_dir)
            locale.AddCatalog("messages")
            gui = Gui(wx.GetTranslation("Logic Simulator"), path, names, devices, network,
                      monitors, language)
            gui.Show(True)
            app.MainLoop()


if __name__ == "__main__":
    main(sys.argv[1:])
