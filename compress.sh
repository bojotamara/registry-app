#!/bin/bash

set -e
set -u

tar -czf prjcode.tgz                     \
    registry.py                          \
    registry_agent.py traffic_officer.py \
    input_util.py                        \
    README.txt Report.pdf
