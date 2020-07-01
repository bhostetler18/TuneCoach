# code adapted from https://packaging.python.org/tutorials/packaging-projects/
from setuptools import setup, find_packages, Extension
from os.path import join

with open("README.md", "r") as fh:
    long_description = fh.read()

sources = ['bridge.cpp', 'TunerStream.cpp', 'PitchDetector.cpp', 'processing_utilities.cpp']
sources_root = './TuneCoach/pitch_detection'
pitch_detection = Extension('TuneCoach.pitch_detection', 
    sources = [join(sources_root, stem) for stem in sources],
    include_dirs = [sources_root],
    libraries = ['pulse-simple'],
    define_macros = [('USE_PULSE', '1')])

setup(
    name="TuneCoach",
    version="0.0.3",
    author="Jamm Hostetler , James Eschrich, Joe Gravelle, Jenny Baik, Gavin Gui",
    author_email="jeschrich@ufl.edu",
    description="An interactive tool for practicing intonation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bhostetler18/TuneCoach/",
    packages=['TuneCoach.gui', 'TuneCoach.python_bridge'],
    py_modules=["TuneCoach.main"],
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    ext_modules=[pitch_detection],
    python_requires='>=3.8',
    install_requires = [
        'numpy>=1.19.0',
        'matplotlib>=3.3.0rc1',
        'Pillow>=7.1.2'
    ],
    include_package_data=True,
    entry_points = {
        'console_scripts': ['TuneCoach=TuneCoach.main:main'],
    }
)
