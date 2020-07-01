# TuneCoach
An interactive tuner that lets musicians practice intonation while performing.

# Install Instructions
## Prerequisites
TuneCoach requires the following libraries to be present in order to be installed:
* ```python3-tk```
* ```libpulse-dev```

You can install them by running
```
$ sudo apt install python3-tk libpulse-dev
```

## Install via PyPI
To install TuneCoach via PyPI, simply run:

```
$ pip install TuneCoach
``` 

The application can now be launched from the terminal with the command ```TuneCoach```.

# Developer Setup

1. Clone the repository
2. Make sure to have ```python3-pip```, ```libpulse-dev```, ```python3-tk```, and (optionally) ```python3-venv``` installed. 
3. (Optional) Set up a virtual environment by running ```python3 -m venv .```
4. Run ```pip install -e .``` to install the application in editable mode (so that changes you make to the source sync to the locally installed package).
5. Run the application by typing ```TuneCoach``` in the terminal.  
