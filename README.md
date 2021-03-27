

# kvrg-avg
A command line utility written in Python for keeping track of central values

## 1. Installation
```bash
sudo curl https://raw.githubusercontent.com/michaelskyba/kvrg-avg/master/main.py -o /usr/bin/avg
sudo chmod +x /usr/bin/avg
```

## 2. Configuration Disclaimer
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

## 3. Usage

- 3.1.1 ``avg create "<name>" ["<description>"]``:
Creates a new tracker called ``<name>`` with an optional description of
``<description>``. If you are creating a regular tracker, do not use "date" as
a description.

- 3.1.2 ``avg list``:
Lists the names of trackers and their average values. This is a human-readable
format; do not attempt to pipe it into something else. If you are invoking
kvrg-avg as part of a script,  use ``avg get`` instead. Typing ``avg`` by
itself is the same as ``avg list``.

- 3.1.3 ``avg delete "<name>"``:
Deletes the tracker called ``<name>``. There is no confirmation prompt; ``avg delete`` is irreversible.

- 3.1.4 ``avg push "<name>" <one or more values>``:
Adds ``<one more values>`` as values to the tracker called ``<name>``. For
example, ``avg push "soda" 2.5 2.5 1`` would add the values 2.5, 2.5, and 1 to
the tracker, "soda". The "soda" tracker (assuming it has no other values) now
has an average of (2.5 + 2.5 + 1)/3 = 2.

- 3.1.5 ``avg get "<attribute>" "<name>"``:
Prints attribute ``<attribute>`` of tracker ``<name>``. List of valid attributes:
    - ``description``
    - ``average``
    - `type`

- 3.1.6 ``avg info "<name>"``:
Prints all attributes of tracker ``<name>``. Like ``avg list``, this is
human-readable and should not be used in a script.

## 3.2 Dates

Dates are a special type of tracker in kvrg-avg. They measure the average
length between entries and can try to predict when the next entry will occur.

- 3.2.1 To create a date tracker, use ``avg create "<name>" date ["<description>"]``.

- 3.2.2 To add an entry to a date tracker, use ``avg push``. However, instead of giving
it a number, you can either give a date in the form "YYYY/MM/DD/HH/MM" (e.g.
2021/01/16/00/15 for Jan 16th 2021, 12:15 AM), or the word "now", which will
input the current date and time. For instance, ``avg push "promotion" now
2020/10/10/01/11`` is valid. If the current date was October 11th 2020, 1:11
AM and the "promotion" tracker had no other entries, the average length between
entries would now be exactly one day.

## 4. Supported Operating Systems

I have developed part of kvrg-avg on Arch Linux and the rest on Gentoo Linux,
so I know it works on both of these, and I believe that it will work fine on
most other Linux distributions (unless /usr/bin/ isn't in your $PATH of course).

kvrg-avg has not been tested on any other Operating Systems, such as BSD or
MacOS, although it should at least function with a few tweaks. The installation
commands I wrote earlier will definitely fail on Windows. If you're using
Windows, you're on your own.

