#!/bin/bash
#
# To Do
# ~~~~~
# - Loop through list of known USB Serial device "/dev/tty*" paths ...
#   - Count number of devices and if there is one device, then use it
#   - Otherwise, display index / devices allowing user to select one

MPF_SCRIPT=$1

$RESET=--reset

mpfshell $RESET -o ${AMPY_PORT:4} -s $MPF_SCRIPT
