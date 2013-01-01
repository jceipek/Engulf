Engulf
======

![Screenshot](https://raw.github.com/jceipek/Engulf/master/screenshot.png "Engulf in action!")

Engulf is a frantic quest to consume nutrients and grow larger while escaping a cloud of enemies. The gameplay and control scheme are finely tuned to take advantage of the Kinect; you must change your avatar's appearance and size in order to eat food of the appropriate color while dodging between narrow gaps formed by enemies harrowing you at every turn.

This day-long project began as an attempt to make a demo for my Python drawing library, [pyShiva](https://github.com/jceipek/pyShiva/). As soon as I connected the library to the Kinect, I knew that I wanted to make a game.


##Gameplay Instructions

###Objective

Collect food particles (pulsing squares) to increase your maximum size.
You can only eat food if its color matches that of your avatar.
Avoid red enemies (when they hit you, they make you shrink)

###Calibration

When the game starts, enter the PSI posture until you are recognized:

        |_O_|
          |
          |
         | |

###Controls

Move your avatar in the 2D plane with your right hand.
Move your right hand closer and further from the Kinect to grow and shrink. 
(Note that if you are too small, your avatar will be grayed out and "locked", unable to consume food.)
Change color by moving your left hand closer and further from the Kinect.


##Requirements

Engulf depends on [pyShiva](https://github.com/jceipek/pyShiva/) for graphics and
[jmendeth's PyOpenNI](https://github.com/jmendeth/PyOpenNI/) for Kinect integration.

##Running

        python engulf.py


##License: GPLv3

Engulf is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Engulf is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Engulf.  If not, see <http://www.gnu.org/licenses/>.