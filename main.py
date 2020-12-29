#!/usr/bin/python

import os
import sys
import subprocess

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

# If config_director/avg/trackers does not exist, create it
# mkdir without -p will raise an error if config_directory/avg doesn't exist first
if not os.path.isdir("f{config_directory}/avg/trackers"):
    subprocess.run(["mkdir", "-p", f"{config_directory}/avg/trackers"])

# Starts checking for command-line arguments

# You ran "avg" without any extra arguments, or you ran "avg list"
# running something like "avg list foo bar" is the same
if len(sys.argv) == 1 or sys.argv[1] == "list":

    # Get the tracker names by looking in config/avg/trackers
    tracker_names = os.listdir(f"{config_directory}/avg/trackers")

    # Alert the user if they have no trackers
    if not tracker_names:
        print("You have no trackers.")
        print("Use 'avg create \"<name>\" [\"<description>\"]' to create one.")

    # Print the tracker names and their average values, if the user has a tracker
    else:
        for tracker in tracker_names:
            print(f"{tracker} - TODO")

