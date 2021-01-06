#This document pulls the latest interop server, performs any modifications based on the dockerfile (if needed), and pushes the new image to AAV's docker account.

#!/bin/bash

docker build -t aavvt/interop:latest .
docker push aavvt/interop:latest
