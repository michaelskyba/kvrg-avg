

# kvrg-avg
A command line utility written in Python for keeping track of central values

## 1. Installation
```sh
git clone https://github.com/michaelskyba/kvrg-avg
su -c "cp kvrg-avg/main.py /usr/local/bin/avg"
```

## 2. Configuration
## 2.1 Disclaimer
By default, kvrg-avg will use files in $HOME/.config/avg. If your
config folder is somewhere else, you will need to open /usr/local/bin/avg
and edit the directory.

Change
```python
config_directory = f"{os.environ['HOME']}/.config"
```
to
```python
config_directory = "<your config directory>"
```
Avoid ending the string with a forward slash.
## 2.2 Config file
The config file will be "(your config directory)/config", so "$HOME/.config/avg/config" by default.
To set an option, just add the name of the option as a line in the file.

- 2.2.1 ``ETA``:
Makes it so that when you run ``avg list``, date trackers will show you the ETA
attribute instead of the average attribute.

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
input the current date and time. For instance, ``avg push "promotion"
2020/10/10/01/11 now`` is valid. If the current date was October 11th 2020, 1:11
AM and the "promotion" tracker had no other entries, the average length between
entries would now be exactly one day. As I showed in the example, you should always
push dates from earliest to latest.

- 3.2.3 When using ``avg list`` or ``avg info`` on date trackers, kvrg-avg will
show the average interval in a human-readable format (e.g. '21 minutes and 42
seconds' instead of '1302'). However, when using ``avg get average`` on a
date tracker, you will receive the number in seconds. This is so that spaces
and "and"s don't get in the way of your script's syntax. You can process the
seconds however you would like.

- 3.2.4 date trackers have a new "ETA" attribute. This is a date that
shows you, based on the average and the last time an entry was made,
approximately when the next entry will occur (assuming the pattern stays the
same, of course, you can't predict the future). ``avg get ETA`` will be in the
form "YYYY-MM-DD HH:MM:SS" (that's the way python's datetime outputs it and I
can't be bothered to make it consistent with the avg push syntax), but
everything else will be in a more human-readable form (e.g. "January 16th, 2008
12:30 PM"). It's possible for the current, real date to be past the ETA. This
means that the next entry was _supposed_ to happen earlier but the pattern
changed.

## 4. Supported Operating Systems

I have developed part of kvrg-avg on Arch Linux and the rest on Gentoo Linux,
so I know it works on both of these, and I believe that it will work fine on
most other Linux distributions (unless /usr/local/bin/ isn't in your $PATH, of course).

kvrg-avg has not been tested on any other Operating Systems, such as BSD or
MacOS, although it should at least function with a few tweaks. The installation
commands I wrote earlier will definitely fail on Windows. If you're using
Windows, you're on your own.

## 5. Bugs

If you find a bug, create an "issue" on GitHub or email me
at michaelskyba1411@gmail.com or michael@michaelskyba.xyz.

## 6. Screenshot

![Screenshot](https://michaelskyba.github.io/kvrg-avg.png)
