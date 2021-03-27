#!/usr/bin/python

import os
import sys
import subprocess
import datetime

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

        if len(sys.argv) > 3 and sys.argv[3] != "date":
            description = sys.argv[3]

        # Date tracker with description

        elif len(sys.argv) > 4:
            description = sys.argv[4]

        # No description

        else:
            description = "This tracker does not have a description."

        # avg create ... date

        if len(sys.argv) > 3 and sys.argv[3] == "date":
            tracker_file.write(f"{description}\n0\n{sys.argv[3]}\n")

        else:
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

    # Check type of tracker
    with open(f"{config_directory}/avg/trackers/{sys.argv[2]}", "r") as tracker_file:
        tracker_lines = tracker_file.readlines()

        if len(tracker_lines) > 2 and tracker_lines[2].strip() == "date":
            tracker_type = "date"
        else:
            tracker_type = "normal"

    # Makes sure all values are numbers if it's a normal tracker
    if tracker_type == "normal":
        for index, argument in enumerate(sys.argv):
            if index > 2:
                try:
                    float_argument = float(argument)
                except ValueError:
                    print(f"Value '{argument}' is not a number.")
                    sys.exit(1)

    # Makes sure all values are dates (or "now") if it's a date tracker
    else:
        for index, argument in enumerate(sys.argv):
            if index > 2:
                # Skip it if they type "now"
                if argument == "now":
                    continue

                # Make sure the date is the right length
                if len(argument) != 16:
                    print(f"Value '{argument}' is invalid.")
                    sys.exit(1)

                # Test if they put slashes in the right places
                for slash in [4, 7, 10, 13]:
                    if argument[slash] != "/":
                        print(f"Value '{argument}' is invalid.")
                        sys.exit(1)

                date = []

                date.append(argument[0:4])
                date.append(argument[5:7])
                date.append(argument[8:10])
                date.append(argument[11:13])
                date.append(argument[14:16])

                # Make sure they put integers as the date values (month, day, etc.)
                for date_index, value in enumerate(date):
                    try:
                        date[date_index] = int(value)

                    except ValueError:
                        print(f"Value '{value}' is not a number.")
                        sys.exit(1)

                # Test if user's date is a real date
                try:
                    final_date = datetime.datetime(date[0], date[1], date[2], date[3], date[4])

                except ValueError:
                    print(f"Value '{argument}' is invalid.")
                    sys.exit(1)

    # Appends values to tracker file
    # A separate loop is used to avoid appending a few of the arguments before
    #   finding out one of them is invalid
    for index, argument in enumerate(sys.argv):
        if index > 2:
            with open(f"{config_directory}/avg/trackers/{sys.argv[2]}", "a") as tracker_file:
                if argument == "now":
                    # cdate -- current date
                    cdate = datetime.datetime.now()
                    # zfill puts in zeros accordingly - '14'.zfill(3) = '014'
                    passed_argument = f"{cdate.year}/{str(cdate.month).zfill(2)}/{str(cdate.day).zfill(2)}/{str(cdate.hour).zfill(2)}/{str(cdate.minute).zfill(2)}"

                else:
                    passed_argument = argument

                tracker_file.write(f"{passed_argument}\n")

    # Update average

    # Calculate the correct average
    with open(f"{config_directory}/avg/trackers/{sys.argv[2]}", "r") as tracker_file:

        new_tracker_file_lines = tracker_file.readlines()

        # Get the number of lines
        tracker_file_num_of_lines = len(new_tracker_file_lines)

        # Normal tracker
        if tracker_type == "normal":
            # Add the values
            value_sum = 0

            for index, value in enumerate(new_tracker_file_lines):
                if index > 1:
                    value_sum += float(value)

            # Actual computation
            average = value_sum * 100 / (tracker_file_num_of_lines - 2)
            average = round(average)
            average = average / 100
            # it needs to be tracker_file_num_of_lines - 2 because the
            #   description (first line) and average (second line) aren't entries

            new_tracker_file_lines[1] = f"{average}\n"

        # Date tracker that has at least two entries
        # You can't calculate an average interval with only one entry, because intervals = entries - 1
        # Date trackers have a description (first line), an average (second line), and a date identifier (third line)
        # That's three lines
        # Finally, the entries are listed. With one entry, you have 3 + 1 = 4 lines
        # So, to have at least two entries, you need to have more than one entry, or more than 4 lines:
        elif tracker_file_num_of_lines > 4:
            # Add the intervals between dates
            # stored as seconds
            intervals = []

            for index, value in enumerate(new_tracker_file_lines):
                # Entries start on the fourth line, so index has to be at least 3
                # lines - 1 is used to avoid later_date being out of range
                if index > 2 and index < (tracker_file_num_of_lines - 1):
                    # print(f"find the distance between {value} and {new_tracker_file_lines[index + 1]}")

                    # Get the earlier date in the right format (index)

                    argument = value

                    date = []
                    date.append(argument[0:4])
                    date.append(argument[5:7])
                    date.append(argument[8:10])
                    date.append(argument[11:13])
                    date.append(argument[14:16])

                    # Make sure everything is an integer
                    int_date = []
                    for part in date:
                        int_date.append(int(part))
                    date = []
                    for part in int_date:
                        date.append(part)

                    earlier_date = datetime.datetime(date[0], date[1], date[2], date[3], date[4])

                    # Get the later date in the right format (index + 1)

                    argument = new_tracker_file_lines[index + 1]

                    date = []
                    date.append(argument[0:4])
                    date.append(argument[5:7])
                    date.append(argument[8:10])
                    date.append(argument[11:13])
                    date.append(argument[14:16])

                    # Make sure everything is an integer
                    int_date = []
                    for part in date:
                        int_date.append(int(part))
                    date = []
                    for part in int_date:
                        date.append(part)

                    later_date = datetime.datetime(date[0], date[1], date[2], date[3], date[4])

                    # Add the interval to the intervals list
                    intervals.append((later_date - earlier_date).total_seconds())

            # calculate the average of the second intervals
            interval_sum = 0

            for interval in intervals:
                interval_sum += interval

            average = interval_sum / (len(intervals))
            average = round(average)

            # write to tracker file
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
    if sys.argv[2] not in ["description", "average", "type", "ETA"]:
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

        # User ran "avg get type <name>"
        if sys.argv[2] == "type":
            if len(tracker_lines) > 2 and tracker_lines[2].strip() == "date":
                print("date")
            else:
                print("normal")

        if sys.argv[2] == "ETA":
            if len(tracker_lines) > 4:
                argument = tracker_lines[len(tracker_lines) - 1].strip()

                date = []
                date.append(argument[0:4])
                date.append(argument[5:7])
                date.append(argument[8:10])
                date.append(argument[11:13])
                date.append(argument[14:16])

                # Make sure everything is an integer
                int_date = []
                for part in date:
                    int_date.append(int(part))
                date = []
                for part in int_date:
                    date.append(part)

                latest_date = datetime.datetime(date[0], date[1], date[2], date[3], date[4])
                average = tracker_lines[1].strip()
                average = int(average)
                average = datetime.timedelta(seconds=average)

                print(latest_date + average)

            else:
                # No intervals
                print("0")

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

        if len(tracker_lines) > 2 and tracker_lines[2].strip() == "date":

            # ETA
            if len(tracker_lines) > 4:
                argument = tracker_lines[len(tracker_lines) - 1].strip()

                date = []
                date.append(argument[0:4])
                date.append(argument[5:7])
                date.append(argument[8:10])
                date.append(argument[11:13])
                date.append(argument[14:16])

                # Make sure everything is an integer
                int_date = []
                for part in date:
                    int_date.append(int(part))
                date = []
                for part in int_date:
                    date.append(part)

                latest_date = datetime.datetime(date[0], date[1], date[2], date[3], date[4])
                average = tracker_lines[1].strip()
                average = int(average)
                average = datetime.timedelta(seconds=average)

                print(f"ETA: {latest_date + average}")

            else:
                # No intervals
                print("ETA: 0")

            # type
            print("This tracker is a date tracker.")
        else:
            print("This is a normal tracker.")

    sys.exit(0)

# Invalid command
print(f"'{sys.argv[1]}' is not a kvrg-avg command. See the README for a list of valid commands.")
sys.exit(1)

