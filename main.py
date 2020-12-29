#!/usr/bin/python

import os
import sys

try:
    # Change the next line if your config folder is not $HOME/.config
    config_directory = f"{os.environ['HOME']}/.config"

    # If $HOME isn't set, os.environ['HOME'] will cause an error
    # We need to tell the user to change the directory

except KeyError:
    print("The environment variable $HOME is not set.")
    print("You need to change the config_directory variable.")
    print("See README.md on github (https://github.com/michaelskyba/kvrg-avg) for more information.")

    sys.exit(1)

# If config_directory doesn't exist, print an error an exit
if not os.path.isdir(config_directory):
    print(f"The config directory that is set ({config_directory}) does not exist.")
    print("You need to change the config_directory variable.")
    print("See README.md on github (https://github.com/michaelskyba/kvrg-avg) for more information.")

    sys.exit(1)

