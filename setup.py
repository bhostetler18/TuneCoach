# code adapted from https://packaging.python.org/tutorials/packaging-projects/
from distutils.core import setup, Extension
from setuptools import find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

pitch_detection = Extension('tunecoach.pitch_detection', 
    sources = ['./tunecoach/pitch_detection/bridge.cpp', './tunecoach/pitch_detection/TunerStream.cpp', \
        './tunecoach/pitch_detection/PitchDetector.cpp', './tunecoach/pitch_detection/processing_utilities.cpp'],
    include_dirs = ['./tunecoach/PitchDetetion'],
    libraries = ['pulse-simple'],
    define_macros = [('USE_PULSE', '1')])

setup(
    name="tunecoach", # Replace with your own username
    version="0.0.1",
    author="Jamm Hostetler , James Eschrich, Joe Gravelle, Jenny Baik, Gavin Gui",
    author_email="jeschrich@ufl.edu",
    description="An interactive tool for practicing intonation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bhostetler18/TuneCoach/",
    packages=['tunecoach.gui', 'tunecoach.python_bridge'],
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    ext_modules=[pitch_detection],
    python_requires='>=3.8',
    install_requires = [
        'numpy',
        'matplotlib'
    ],
    include_package_data=True
)
