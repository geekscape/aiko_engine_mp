#!/bin/bash

rm -f .install.mpf
for i in *.py *.pbm
do
    if [ "$i" -nt ."$i".pushed ]; then
	cat >> .install.mpf << EOF
exec print("$i")
put $i examples/$i
EOF
	touch ."$i".pushed
    fi
done

# FIXME for your architecture
test -e  .install.mpf && mpfshell ttyUSB0 -s .install.mpf
