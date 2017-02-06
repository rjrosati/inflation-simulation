# inflation-simulation
Have you ever wondered "How far away can my screams reach?"? Well, here is the ultimate answer. It doesn't get any less causally connected than this. Here we introduce INFLATION SIMULATOR 9000. Be it that you started screaming at the beggining of the universe, of rather late (during radiation dominated era) we can tell you how far away they will ever reach!

A little `pygame` animation showing the evolution of the causal horizon during cosmic inflation.

The simulation will begin paused.
+ <kbd>SPACE</kbd> starts/pauses the simulation.
+ Left clicks release a shell of light where you click.
+ <kbd>p</kbd> toggles the plot of a(t) 
+ <kbd>h</kbd> toggles the display of the causal horizon (i.e. the max comoving distance the current light ray could travel in infinite time) 
+ <kbd>r</kbd> resets the simulation to the initial conditions at t=0
+ <kbd>g</kbd> GODMODE, sets view to comoving coordinates.
+ <kbd>e</kbd> ends inflation and switches to radiation domination
+ <kbd>m</kbd> toggles music 
+ <kbd>ENTER</kbd> speeds up time by a factor of 10 while held down

Things to try:

- Causal horizon:
Switch to GODMODE. Start a light beam. Notice how the light beam will never reach the causal horizon. End inflation. Causal horizon will disappear, why do you think that is?
- Look at the plot.

Some warnings:
We are not solving the full FRW equations here, especially not when switching from inflation to radiation domination.
If we solved the full equations of motion, we wouldn't be able to stay in inflation arbitrarily long.
You might notice some irregularites if you end inflation before a(t)=10 or so (like light going backwards).
This is an artefact of the approximations we are using and isn't physical. 
If anyone has an easy fix, feel free to message or submit a pull request.

The music is Hybrid Song from TeleportProkg.
