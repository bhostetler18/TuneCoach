from distutils.core import setup, Extension

# with open("README.md", "r") as fh:
#     long_description = fh.read()

pitch_detection = Extension('pitch_detection', 
    sources = ['./PitchDetection/bridge.cpp', './PitchDetection/TunerStream.cpp', './PitchDetection/PitchDetector.cpp', \
        './PitchDetection/processing_utilities.cpp'],
    include_dirs = ['./PitchDetetion'],
    libraries = ['pulse-simple'],
    define_macros = [('USE_PULSE', '1')])

setup(
    name="tunecoach", # Replace with your own username
    version="0.0.1",
    author="Jamm Hostetler , James Eschrich, Joe Gravelle, Jenny Baik, Gavin Gui",
    author_email="TODO",
    description="An interactive tool for practicing intonation",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    # packages=["gui"],
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    ext_modules=[pitch_detection],
    python_requires='>=3.8',
)
