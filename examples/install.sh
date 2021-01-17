#!/bin/bash

rm -f .install.mpf
for i in *.py *.pbm
do
    if [ "$i" -nt ."$i".pushed ]; then
	cat >> .install.mpf << EOF
exec print("$i")
put $i examples/$i
EOF
    fi
done

# FIXME for your architecture
test -e  .install.mpf && mpfshell ttyUSB0 -s .install.mpf 2>&1 | tee .install.mpf.output
grep -q "Not connected to device" .install.mpf.output && exit

# only update the touch markers if the push was successful
for i in *.py *.pbm
do
    if [ "$i" -nt ."$i".pushed ]; then
	echo "Pushed $i, updating last push time"
	touch ."$i".pushed
    fi
done
