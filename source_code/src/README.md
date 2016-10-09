Laser pointer control with Stellarium
========================================
Yash Bhalgat | Kalpesh Patil | Meet Shah


This project consists on a first approach to control a pan-tilt mechanism, built from scratch and
based on Arduino microcontrolle and the Stellarium software.

Software
---------

The software is divided on two main blocks, the first one implemented in Python (computer) and the other
one for Arduino microcontroller (device):

In the computer side with Python:

* Communications with Stellarium ([Stellarium Telescope Protocol](http://www.stellarium.org/wiki/index.php/Telescope_Control_(client-server\)), [python-bitstring](http://code.google.com/p/python-bitstring/))
* Communications with the device (USB-Serial)
* User interface (PyQt4)

Device with Arduino:

* Communications with the computer (receiving commands and parameters, and sending responses)
* Control mechanisms (servo motors, laser positioning)


### python folder

Software to control the "Laser pointer device" with Stellarium, including GUI.


### bitstring-3.0.2 folder

A Python module that makes the creation, manipulation and analysis of binary data as simple and natural as possible.
Bitstring project page: http://code.google.com/p/python-bitstring/


### arduino folder

code for pan-tilt mechanism, laser pointer control handling and two-way communication.
...to be uploaded on arduino.
