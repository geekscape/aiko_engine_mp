#!/bin/bash

DEST=examples/

rm -f .install.mpf

for i in *.py *.pbm
do
    if [ "$i" -nt ."$i".pushed ]; then
	if [[ $i =~ .py$ ]]; then 
	    python -m py_compile "$i" || exit
	fi
	cat >> .install.mpf << EOF
exec print("$i")
put $i $DEST/$i
EOF
    fi
done

# FIXME for your architecture
test -e  .install.mpf && mpfshell ttyUSB0 -s .install.mpf 2>&1 | tee .install.mpf.output
grep -q "Not connected to device" .install.mpf.output && exit
grep -q "Failed to create file" .install.mpf.output && echo "You will need to manually run md $DEST once" && exit

# only update the touch markers if the push was successful
for i in *.py *.pbm
do
    if [ "$i" -nt ."$i".pushed ]; then
	echo "Pushed $i, updating last push time"
	touch ."$i".pushed
    fi
done

cat <<EOF
Type this in repl for space left:
import os; print(os.statvfs("/")[0]*os.statvfs("/")[3], "bytes free out of",os.statvfs("/")[1]*os.statvfs("/")[2])
EOF
