# AAV's Files for Interop Integration
This repository includes all the files used in addition to the base AUVSI SUAS Interoperabilty System (Interop). The base AUVSI SUAS Interop documentation can be found [here](https://github.com/auvsi-suas/interop). The following programs must be installed:

- [Docker](https://docs.docker.com/get-started/)
- [Mavproxy](https://ardupilot.org/mavproxy/docs/getting_started/download_and_installation.html#)

## Interacting with Interoperability
There are two ways to connect to interop based on the resources at hand: SITL or HITL. Steps on how to run the simulator can be found here. Ensure that the aircraft is powered on or the simulator is running before trying to establish a connection.

### Connecting to Interoperability

The following script can be used to connect to Interop and retrieve mission information. When working with a simulator the --master port should be denoted as the simulation output IP address (default: tcp:127.0.0.1:5760) instead of the USB port (ttyUSB#).

```
mavproxy.py --master=/dev/ttyUSB# --out=udp:127.0.0.1:14550 --out=udp:10.10.130.99:14551
sudo docker run --net=host --interactive --tty aavvt/interop:latest
sudo python ./tools/interop_cli.py --url http://INTEROP_SERVER_IP --username USERNAME --password PASSWORD mission --mission_id MISSION_ID
connect mission planner to 10.10.130.99:14551
```

### Converting Mission Data

Once the mission data is received, run the interop.py file and paste in the mission data dictionary. This should result in multiple files that can be uploaded to mission planner.

### Submitting Data to Interoperability

The following line is used to submit **aircraft data** to the server:
```
sudo python ./tools/interop_cli.py --url http://INTEROP_SERVER_IP --username USERNAME --mission_id MISSION_ID mavlink --device 127.0.0.1:14550
```
The following line is used to submit **ODLC data** to the server:
```
sudo python ./tools/interop_cli.py --url http://INTEROP_SERVER_IP --username USERNAME --mission_id MISSION_ID odlcs --odlc_dir /PATH/TO/OBJECT/DIRECTORY
```
The following line is used to submit your **final map** to the server: 
```
sudo python ./tools/interop_cli.py --url http://INTEROP_SERVER_IP --username USERNAME --mission_id MISSION_ID map --map_filepath /PATH/TO/MAP/DIRECTORY
```

## Updating AAV's Docker Hub Image

By running the update.bat file - custom modifications are made to the latest AUVSI SUAS Interop and pushed to AAV's Docker Hub. This automated process should be run every time a the base AUVSI SUAS Interop has been updated by the competition.

There are currently no modifications being made by AAV to the base AUVSI SUAS Interop. Since no modifications are currently being made, there is no crucial reasoning behind have a team-specific version of the Interop scripts. However, in the past AAV has been required to make slight changes and this may be required again in the future. Thus, the process for implementing these changes still resides in this documentation.


## Tips and Tricks

- When you receive interopeability details at checkin (INTEROP_SERVER_IP, USERNAME, PASSWORD, etc.), copy the above lines and modify them to include the exact information. This will make server integration easier when at the flight line.

- Max sure that all altitude values in the waypoint mission output as absolute. This should be done automatically by the interop.py file.

- Simulation setup is being modified and can be found on another repo soon!
