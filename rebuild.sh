#/bin/bash
docker build -t cewuandy/serviceone-synchronizer -f Dockerfile.synchronizer .
docker push cewuandy/serviceone-synchronizer

