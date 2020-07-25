#!/bin/sh

MPF_SCRIPT=$1

mpfshell --reset -o ${AMPY_PORT:4} -s $MPF_SCRIPT
