# Surround.py: A Framework for Immersive Spatial Audio Simulation and Education

[ [Link to Paper](https://drive.google.com/file/d/1OJ-hxY4pB_YSWVjqa-5KIeeadIcZRsNg/view) ]
Author: Varun Shenoy (vnshenoy@stanford.edu)

Affiliation: Dept. of Electrical Engineering, Stanford University

## Project File Structure

- `requirements.txt` contains all the dependencies necessary to run this project. You can use conda or pip to install the exact versions of dependencies which we used from this file.
- The `sounds` folder contains various sample sounds from mixkit (https://mixkit.co/free-sound-effects/). You can add any sounds you want to try here, but make sure that they are 16 bit. You can use an online converter (https://audio.online-convert.com/convert-to-wav) to change a sound's bit resolution to 16 bit.
- The `hrtf` folder contains the entire KEMAR HRIR dataset from MIT. Information about this dataset can be found here: https://sound.media.mit.edu/resources/KEMAR.html.
- The `code` folder contains all the source files for the project.
    - `Speakers.py` houses the `BasicSpeaker`, `HRTFSpeaker`, and `AmbisonicsSpeakers` classes that are the bread and butter of this package.
    - `Soundstage.py` includes the `Soundstage` class and its various methods. The `plot` method is particularly comprehensive.
    - `utils.py` has several helper functions for interfacing with pydub, numpy, and the KEMAR dataset.
    - Take a look at the various demo files to see how this framework is used in action.

# Running the project

I built this project on Python 3.8.11, but it might work on earlier versions.

After `cd`-ing into the main folder, install the prerequisite frameworks using `pip install -r requirements.txt` or your desired package manager.

Then, `cd` into the `code` folder and run `python3 demo-hrtf.py` or any other demo file that is already there (or one that you have created)!
