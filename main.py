#!/usr/bin/python

import os
import sys
import subprocess

try:
    # Change the next line if your config folder is not $HOME/.config
    config_directory = f"{os.environ['HOME']}/.config"

    # If $HOME isn't set, os.environ['HOME'] will cause an error

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
        sys.exit(1)

    # Print the tracker names and their average values, if the user has a tracker
    else:
        for tracker in tracker_names:
            with open(f"{config_directory}/avg/trackers/{tracker}", "r") as tracker_file:
                print(f"{tracker} - {tracker_file.readlines()[1].strip()}")
        sys.exit(0)

# You ran "avg create ..."
if sys.argv[1] == "create":
    # If user runs "avg create"
    if len(sys.argv) == 2:
        print("You need a <name> argument.")
        sys.exit(1)

    # Check if config/avg/trackers contains a tracker called <name>
    if sys.argv[2] in os.listdir(f"{config_directory}/avg/trackers"):
        print(f"Tracker with name '{sys.argv[2]}' already exists.")
        sys.exit(1)

    # Create a file with name <name> in config/avg/trackers
    with open(f"{config_directory}/avg/trackers/{sys.argv[2]}", "w") as tracker_file:

        # Saves the description if the user provided one

        # the description is the fourth argument, so the length has to be > 3 (>=4)
        # and sys.argv[3] will get the fourth argument (3rd when not including "avg")
        if len(sys.argv) > 3:
            description = sys.argv[3]
        else:
            description = "This tracker does not have a description."

        tracker_file.write(f"{description}\n0\n")

    sys.exit(0)

# You ran "avg delete ..."
if sys.argv[1] == "delete":
    # If user runs "avg delete"
    if len(sys.argv) == 2:
        print("You need a <name> argument.")
        sys.exit(1)

    # Removes the tracker file
    try:
        os.remove(f"{config_directory}/avg/trackers/{sys.argv[2]}")

    # Tracker does not exist
    except FileNotFoundError:
        print(f"There is no such tracker '{sys.argv[2]}'.")
        sys.exit(1)

    sys.exit(0)

# You ran "avg push ..."
if sys.argv[1] == "push":
    # If user runs "avg push"
    if len(sys.argv) == 2:
        print("You need a <name> and a <one or more values> argument.")
        sys.exit(1)

    # Check if config/avg/trackers contains a tracker called <name>
    if sys.argv[2] not in os.listdir(f"{config_directory}/avg/trackers"):
        print(f"Tracker with name '{sys.argv[2]}' does not exist.")
        sys.exit(1)

    # If user runs "avg push <name>"
    if len(sys.argv) == 3:
        print("You need a <one or more values> argument.")
        sys.exit(1)

    # Makes sure all values are numbers
    for index, argument in enumerate(sys.argv):
        if index > 2:
            try:
                float_argument = float(argument)
            except ValueError:
                print(f"Value '{argument}' is not a number.")
                sys.exit(1)

    # Appends values to tracker file
    # A separate loop is used to avoid appending a few of the arguments before
    # finding out one of them in invalid
    for index, argument in enumerate(sys.argv):
        if index > 2:
            with open(f"{config_directory}/avg/trackers/{sys.argv[2]}", "a") as tracker_file:
                tracker_file.write(f"{argument}\n")

    # Update average

    # Calculate the correct average
    with open(f"{config_directory}/avg/trackers/{sys.argv[2]}", "r") as tracker_file:
        # Add the values
        value_sum = 0

        new_tracker_file_lines = tracker_file.readlines()

        for index, value in enumerate(new_tracker_file_lines):
            if index > 1:
                value_sum += float(value)

        # Get the number of lines
        tracker_file_num_of_lines = len(new_tracker_file_lines) - 2

        # Actual computation
        average = value_sum * 100 / tracker_file_num_of_lines
        average = round(average)
        average = average / 100

        new_tracker_file_lines[1] = f"{average}\n"

    # Update the average in the file
    with open(f"{config_directory}/avg/trackers/{sys.argv[2]}", "w") as tracker_file:
        tracker_file.writelines(new_tracker_file_lines)

    sys.exit(0)

# You ran "avg get ..."
if sys.argv[1] == "get":
    # If user runs "avg get"
    if len(sys.argv) == 2:
        print("You need an <attribute> argument and a <name> argument.")
        sys.exit(1)

    # Check if user gave a valid attribute
    if sys.argv[2] not in ["description", "average"]:
        print(f"No such attribute, '{sys.argv[2]}'.")
        sys.exit(1)

    # If user runs "avg get <attribute>"
    if len(sys.argv) == 3:
        print("You need a <name> argument.")
        sys.exit(1)

    # Checks if user gave a valid tracker name
    if sys.argv[3] not in os.listdir(f"{config_directory}/avg/trackers"):
        print(f"Tracker with name '{sys.argv[3]}' does not exist.")
        sys.exit(1)

    # Use has a valid tracker name
    with open(f"{config_directory}/avg/trackers/{sys.argv[3]}", "r") as tracker_file:
        tracker_lines = tracker_file.readlines()

        # User ran "avg get description <name>"
        if sys.argv[2] == "description":
            print(tracker_lines[0].strip())

        # User ran "avg get average <name>"
        if sys.argv[2] == "average":
            print(tracker_lines[1].strip())

    sys.exit(0)

# You ran "avg info ..."
if sys.argv[1] == "info":
    # If user runs "avg info"
    if len(sys.argv) == 2:
        print("You need a <name> argument.")
        sys.exit(1)

    # Checks if user gave a valid tracker name
    if sys.argv[2] not in os.listdir(f"{config_directory}/avg/trackers"):
        print(f"Tracker with name '{sys.argv[2]}' does not exist.")
        sys.exit(1)

    # Lists attributes
    with open(f"{config_directory}/avg/trackers/{sys.argv[2]}", "r") as tracker_file:
        tracker_lines = tracker_file.readlines()

        print(f"Name: {sys.argv[2]}")
        print(f"Description: {tracker_lines[0].strip()}")
        print(f"Average: {tracker_lines[1].strip()}")


    sys.exit(0)

# Invalid command
print(f"'{sys.argv[1]}' is not a kvrg-avg command. See the README for a list of valid commands.")
sys.exit(1)

