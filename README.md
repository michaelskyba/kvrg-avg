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
and change the directory.
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
Do not end your directory with a forward slash.
