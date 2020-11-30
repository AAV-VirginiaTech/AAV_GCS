# Team Specific Files for Interop Integration
This repository includes all the files used in addition to the base AUVSI SUAS Interoperabilty System (Interop). AAV only makes modifications to the client side and uses an unmodified version of the server side for all integration testing. The base AUVSI SUAS Interop documentation can be found [here](https://github.com/auvsi-suas/interop).


## Modifications to Base Client Script

By running the deploy.bat file - custom modifications are made to the latest AUVSI SUAS Interop and pushed to AAV's Docker Hub. For full steps as to how to run the modifications, please see the following [steps](https://docs.google.com/spreadsheets/u/1/d/19mjOYNVK9p9t9GF8WmlmqMOV-TGl6wsb1qi4te709V4/edit?usp=drive_web&ouid=103418167026044020491). This automated process should be run every time a the base AUVSI SUAS Interop has been updated by the competition.

The following modifications are currently made to the system:
- MSL Altitude to AGL Altitude + 22' (See Changes to mavlink_proxy.py)


## Connecting to Interoperability
There are three ways to connect to interop based on the given environment: competition, HITL, SITL. Altough similar, each setup process has been detailed below.

**Connecting to Interoperability (Competition)**
The following lines can be used to connect to interop and begin streaming information to the server at competition:

sudo docker run --net=host --interactive --tty aavvt/interop:latest

sudo python ./tools/interop_cli.py --url http://10.10.130.10:80 --username USERNAME --password PASSWORD mission --mission_id MISSION_ID

*Open a New Terminal and CD to the MavProxy Directory*

sudo python mavproxy.py --master=/dev/ttyUSB# --out=udp:127.0.0.1:14550 --out=udpout:10.10.130.93:14551

*Return to the Interop Script Terminal*

sudo python ./tools/interop_cli.py --url http://10.10.130.10:80 --username virginiatech --password 3391799053 mavlink --device 127.0.0.1:14550




**Connecting to Interoperability (HITL Testing)**

**Connecting to Interoperability (SITL Testing)**

Link to Connecting to Interop Steps: https://docs.google.com/document/u/1/d/1K8JhXIW9-weg4ZLH8XjKiC9EUNEVvPcUT6Bc2LuULR4/edit?usp=drive_web&ouid=103418167026044020491
