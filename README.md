# inflation-simulation
Have you ever wondered "How far away will my screams reach?"? Well, here is the ultimate answer. It doesn't get any less causally connected than this. Here we introduce INFLATION SIMULATOR 9000. Be it that you started screaming at the beggining of the universe, of rather late (during radiation dominated era) we can tell you how far away they will ever reach!

# Download
(Easiest) To run a pre-compiled version of the game on Mac or Linux, download and unzip 
this file: https://github.com/rjrosati/inflation-simulation/releases/download/v0.1/game.zip . Then double-click the file named `runme`.

(Run from source)
To download this script, click on the green "clone or download" button right above the list of files. If you have `git` installed, you can clone the repository, or you can download the current version as a zip file.

# Installation
This script uses the `Python` libraries `numpy` and `pygame`. If you have `Python` installed, but without these libraries, the easiest way to get them is through `pip`. See https://packaging.python.org/installing/#use-pip-for-installing .

If you don't have `Python` installed, we recommend you install the Anaconda distribution (for Python 2), which comes prepackaged with these libraries. https://www.continuum.io/downloads

# Running the script from source
On Mac or Linux, open a terminal in the script's folder and type 
```bash
$> python ./universe.py
```

On Windows, hold down <kbd>Shift</kbd> and right-click in the script's folder. Choose "Open Command Window Here". Type:
```cmd
C:\Users\...\inflation-simulation> python universe.py
```

# Controls
The simulation will begin paused.
+ <kbd>SPACE</kbd> starts/pauses the simulation.
+ <kbd>ENTER</kbd> speeds up time by a factor of 10 while held down
+ <kbd class="mouse">Left click</kbd> release a shell of light where you click.
+ <kbd>p</kbd> toggles the plot of a(t) 
+ <kbd>h</kbd> toggles the display of the causal horizon (i.e. the max comoving distance the current light ray could travel in infinite time) 
+ <kbd>e</kbd> ends inflation and switches to radiation domination
+ <kbd>g</kbd> GODMODE, sets view to comoving coordinates.
+ <kbd>r</kbd> resets the simulation to the initial conditions at t=0
+ <kbd>m</kbd> toggles music 

# Things to try:

- Causal horizon:
Switch to GODMODE. Start a light beam. Notice how the light beam will never reach the causal horizon. End inflation. Causal horizon will skyrocket, why do you think that is?
- Look at the plots in the two modes: 
NOTICE THE INTERSECTIONS: Your screams could hardly be heard during inflation but radiation era brings them back to those distant places!!!

Some warnings:
We are not solving the full FRW equations here, especially not when switching from inflation to radiation domination.
If we solved the full equations of motion, we wouldn't be able to stay in inflation arbitrarily long.
You might notice some irregularites if you end inflation before a(t)=10 or so (like light going backwards).
This is an artefact of the approximations we are using and isn't physical. 
If anyone has an easy fix, feel free to message or submit a pull request.

The music is Hybrid Song from TeleportProkg.
