#!/bin/bash

python3 main.py generate -t il > toplevel.il
sby -f "$1"
