PyBrew
======

This is a basic system helps control the temperature of a homebrew while it's
fermenting. The CO2 emission monitor is a WIP and completely non-functional.

Temperature Control
-------------------

The setup consists of:

- RaspberryPI (the monitor/control brain)
- digital thermometer (DS18B20)
- Submersible heating element
- Water pump
- Copper coiling

The digital thermometer is submersed in the fermentation bucket.
The copper coiling is wrapped around the fermentation bucket and each end is
plugged into a container with ~1-2L water. The output of the pump is attached
to one end of the coil and the other end sits in the water.

If the temperature falls below a certain threshold, then the pump and heater
are activated. If if goes above a certain threshold, then the pump and heater
are deactivated.

CO2
---
The intention there is to use a sensitive laser (from e.g. a computer mouse)
that will be disturbed by a bubble of CO2 going through the airlock.

Server side monitoring
----------------------

The RaspberryPI monitor also sends metrics to a server for the following
events:

- Temperature change
- Pump activation/deactivation
- Heater activation/deactivation
