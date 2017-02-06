# inflation-simulation
A little `pygame` animation showing the evolution of the causal horizon during cosmic inflation.

The simulation will begin paused.
+ <kbd>SPACE</kbd> starts/pauses the simulation.
+ Left clicks release a shell of light where you click.
+ <kbd>p</kbd> toggles the plot of a(t) 
+ <kbd>h</kbd> toggles the display of the particle horizon (i.e. the max comoving distance the current light ray could travel in infinite time) 
+ <kbd>r</kbd> resets the simulation to the initial conditions at t=0
+ <kbd>e</kbd> ends inflation and switches to radiation domination
+ <kbd>m</kbd> toggles music 
+ <kbd>ENTER</kbd> speeds up time by a factor of 10 while held down

Some warnings:
I'm not solving the full FRW equations here, especially not when switching from inflation to radiation domination.
If I solved the full equations of motion, I wouldn't be able to stay in inflation arbitrarily long.
You might notice some irregularites if you end inflation before a(t)=10 or so (like light going backwards).
This is an artefact of the approximations I'm using and isn't physical. 
If anyone has an easy fix, feel free to message me or submit a pull request.

The music is Hybrid Song from TeleportProkg.
