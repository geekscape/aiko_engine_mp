#!/bin/bash

> .install.mpf
for i in *.py *.pbm
do
    cat >> .install.mpf << EOF
exec print("$i")
put $i examples/$i
EOF
done

# FIXME for your architecture
mpfshell ttyUSB0 -s .install.mpf
