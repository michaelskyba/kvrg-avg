

# kvrg-avg
A command line utility written in Python for keeping track of central values

## Installation
```bash
sudo curl https://raw.githubusercontent.com/michaelskyba/kvrg-avg/master/main.py -o /usr/bin/avg
sudo chmod +x /usr/bin/avg
```

## Configuration Disclaimer
By default, kvrg-avg will use files in $HOME/.config/avg. If your
config folder is somewhere else, you will need to open /usr/bin/avg
and edit the directory.
```bash
sudo -e /usr/bin/avg
```
Change
```python
config_directory = f"{os.environ['HOME']}/.config"
```
to
```python
config_directory = "<your config directory>"
```
Avoid ending the string with a forward slash.

## Usage

 -  ``avg create "<name>" ["<description>"]``:
Creates a new tracker called ``<name>`` with an optional description of
``<description>``. If you are creating a regular tracker, do not use "date" as
a description.

- ``avg list``:
Lists the names of trackers and their average values. This is a human-readable
format; do not attempt to pipe it into something else. If you are invoking
kvrg-avg as part of a script,  use ``avg get`` instead. Typing ``avg`` by
itself is the same as ``avg list``.

- ``avg delete "<name>"``:
Deletes the tracker called ``<name>``. There is no confirmation prompt; ``avg delete`` is irreversible.

- ``avg push "<name>" <one or more values>``:
Adds ``<one more values>`` as values to the tracker called ``<name>``. For example, ``avg push "soda" 2.5 2.5 1`` would add the values 2.5, 2.5, and 1 to the tracker, "soda". The "soda" tracker (assuming it has no other values) now has an average of (2.5 + 2.5 + 1)/3 = 2.

- ``avg get "<attribute>" "<name>"``:
Prints attribute ``<attribute>`` of tracker ``<name>``. List of valid attributes:
    - ``description``
    - ``average``
    - `type`

- ``avg info "<name>"``:
Prints all attributes of tracker ``<name>``. Like ``avg list``, this is human-readable and should not be used in a script.

- **Dates**:
Dates are a special type of tracker in kvrg-avg. They measure the average length between entries and can try to predict when the next entry will occur. To create a date tracker, use ``avg create "<name>" date ["<description>"]``.
