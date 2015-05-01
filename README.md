# oleardusim

    This is an old (2011) implementation of an HIL simulation that I did.
    Python provides the connection betwween the ArduPilot 2.0 hardware (arduino, basically),
    IMU, GPS, etc and XPlane.  The implementation was very much in development at the time
    and has lots of things that need to be completed.  

## What's done ##

    As far as I remember, you can hook up a single ArduPilot2 board, fly it in various modes, 
    allow it to recover from dives/crash-scenarios and the like

## What's not done ##

    There's a server and the beginnings of the ability to manage multiple ArduPilot boards, but 
    at this time, you can only use one.  Parallelism is improperly implemented.  A GUI needs to 
    be completed.




