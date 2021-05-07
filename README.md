# AAV's Files for Interop Integration
This repository includes all the files used in addition to the base AUVSI SUAS Interoperabilty System (Interop). The base AUVSI SUAS Interop documentation can be found [here](https://github.com/auvsi-suas/interop). The following programs must be installed:

- [Docker](https://docs.docker.com/get-started/)
- [Mavproxy](https://ardupilot.org/mavproxy/docs/getting_started/download_and_installation.html#)

## Connecting to Interoperability
There are two ways to connect to interop based on the resources at hand: SITL or HITL. Docker Desktop must be running prior to running any of the following scripts.

#### Connecting to Interoperability (HITL)

The following script can be used to connect to Interop and begin streaming information to the server with a UAV:
```
mavproxy.py --master=/dev/ttyUSB# --out=udp:127.0.0.1:14550 --out=udp:10.10.130.99:14551
sudo docker run --net=host --interactive --tty aavvt/interop:latest
sudo python ./tools/interop_cli.py --url http://INTEROP_SERVER_IP --username USERNAME --password PASSWORD mission mavlink --device 127.0.0.1:14550 --mission_id MISSION_ID
connect mission planner to 10.10.130.99:14551
```

#### Connecting to Interoperability (SITL)

The following script can be used to connect to Interop and begin streaming information to the server with a **simulated** UAV:
```
sudo python Sim_Drone.py
mavproxy.py --master=tcp:127.0.0.1:5760 --out=udp:127.0.0.1:14550 --out=udp:10.10.130.99:14551
sudo docker run --net=host --interactive --tty aavvt/interop:latest
sudo python ./tools/interop_cli.py --url http://INTEROP_SERVER_IP --username USERNAME --password PASSWORD mission mavlink --device 127.0.0.1:14550 --mission_id MISSION_ID
connect mission planner to 10.10.130.99:14551
```

## Updating AAV's Docker Hub Image

By running the update.bat file - custom modifications are made to the latest AUVSI SUAS Interop and pushed to AAV's Docker Hub. This automated process should be run every time a the base AUVSI SUAS Interop has been updated by the competition.

There are currently no modifications being made by AAV to the base AUVSI SUAS Interop. Since no modifications are currently being made, there is no crucial reasoning behind have a team-specific version of the Interop scripts. However, in the past AAV has been required to make slight changes and this may be required again in the future. Thus, the process for implementing these changes still resides in this documentation.
