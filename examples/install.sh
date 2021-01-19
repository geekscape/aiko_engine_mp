#!/bin/bash
#
# microPython v1.13 is effectively Python 3.4.0
# Please ensure that your host Python version is Python 3.4 or newer
# Otherwise the host side compilation check may fail on some source code

TTY=${1:-ttyUSB0}
DEST=${2:-$(pwd | sed "s#.*aiko_engine_mp/##")}

mkdir -p .inst
rm -f .inst/.install.mpf

for i in *.py *.pbm
do
    if [ "$i" -nt .inst/"$i".pushed ]; then
	if [[ $i =~ .py$ ]]; then 
	    python3 -m py_compile "$i" || exit
	fi
	cat >> .inst/.install.mpf << EOF
exec print("$i")
put $i $DEST/$i
EOF
    fi
done

# FIXME for your architecture
test -e  .inst/.install.mpf && mpfshell $TTY -s .inst/.install.mpf 2>&1 | tee .inst/.install.mpf.output
grep -q "Not connected to device" .inst/.install.mpf.output && exit
grep -q "Failed to create file" .inst/.install.mpf.output && echo "You will need to manually run md $DEST once" && exit

# only update the touch markers if the push was successful
for i in *.py *.pbm
do
    if [ "$i" -nt .inst/"$i".pushed ]; then
	#echo "Pushed $i to $DEST, updating last push time"
	touch .inst/"$i".pushed
    fi
done

if type pyboard.py &>/dev/null; then 
    pyboard.py --device /dev/$TTY -c 'import os; print(os.statvfs("/")[0]*os.statvfs("/")[3], "bytes free out of",os.statvfs("/")[1]*os.statvfs("/")[2])'
else
    echo "Consider installing pyboard.py in your path (pip install rshell or https://github.com/micropython/micropython/blob/master/tools/pyboard.py )"
fi
