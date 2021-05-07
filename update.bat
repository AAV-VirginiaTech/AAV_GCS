#This document pulls the latest AUVSI SUAS interop image, performs any modifications based on the dockerfile (if needed), and pushes the new image to AAV's docker account.

#!/bin/bash

docker build -t auvsisuas/interop-client:latest .
docker push aavvt/interop:latest
