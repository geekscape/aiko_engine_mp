#!/bin/bash
#
# Setup
# ~~~~~
# KEYS_PATHNAME=z_keys
# START=1
# LENGTH=5
# mkdir $KEYS_PATHNAME
# echo $START >$KEYS_PATHNAME/index
# ./scripts/generate_keys.sh $KEYS_PATHNAME $START $LENGTH
#
# Flash device with unique encryption key
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ./scripts/flash_swagbadge.sh

CONFIGURATION_KEY_FILENAME=configuration/keys.db
KEYS_PATHNAME=z_keys
KEYS_INDEX=$KEYS_PATHNAME/index
KEYS_LOG_PATHNAME=$KEYS_PATHNAME/allocated_keys.log

# If not already saved, then save default "configuration/keys.db"
#
if [ ! -f "${CONFIGURATION_KEY_FILENAME}_default" ]; then
  mv $CONFIGURATION_KEY_FILENAME ${CONFIGURATION_KEY_FILENAME}_default 2>/dev/null
fi

# Determine next "keys_$INDEX.db" file to use
#
INDEX=0000`cat $KEYS_INDEX`
INDEX=${INDEX: -4}
KEYS_FILENAME=$KEYS_PATHNAME/keys_$INDEX.db

# Check if "keys_$INDEX.db" file exists
#
if [ ! -f "$KEYS_FILENAME" ]; then
  echo "$KEYS_FILENAME does not exist, you've run out of unique keys !"
  exit
fi

# Use unique "keys_$INDEX.db" when flashing ESP32
#
cp $KEYS_FILENAME $CONFIGURATION_KEY_FILENAME
echo "Index is $INDEX and using $KEYS_FILENAME"
echo "###########################################"

# Erase, flash microPython and flash Aiko Engine to ESP32
#
./scripts/flash_micropython.sh
./scripts/mpf_script.sh ./scripts/aiko.mpf
echo "###########################################"

# Display the unique key INDEX (up-one integer) and ESP32 serial id
#
DEVICE_SERIAL_ID=`./scripts/device_info.py $AMPY_PORT 2>&1 | grep passed | cut -d\' -f2`
echo "Index is $INDEX for ESP32 serial id: $DEVICE_SERIAL_ID"

# Increment unique key index value
#
INDEX=`cat $KEYS_INDEX`
echo `expr $INDEX + 1` >$KEYS_INDEX

# Update allocated keys log file "INDEX:DEVICE_SERIAL_ID"
# Record count should increment by one, each time
#
touch $KEYS_LOG_PATHNAME
KEYS_LOG_OLD_LENGTH=`wc -l $KEYS_LOG_PATHNAME | column -t | cut -d" " -f1`
KEYS_LOG_OUTPUT="$INDEX:$DEVICE_SERIAL_ID"
echo $KEYS_LOG_OUTPUT >>$KEYS_LOG_PATHNAME
KEYS_LOG_NEW_LENGTH=`wc -l $KEYS_LOG_PATHNAME | column -t | cut -d" " -f1`
echo "$KEYS_LOG_PATHNAME record count: $KEYS_LOG_OLD_LENGTH -> $KEYS_LOG_NEW_LENGTH"

DUPLICATES_COUNT=`cut -d: -f1 $KEYS_LOG_PATHNAME | sort | uniq -d | wc -l | column -t`
if [ $DUPLICATES_COUNT -eq 0 ]; then
    echo "No duplicate key index used :)"
else
    echo "ERROR: Duplicate key index count: $DUPLICATES_COUNT"
    DUPLICATES=`cut -d: -f1 $KEYS_LOG_PATHNAME | sort | uniq -d | xargs echo`
    echo "ERROR: Duplicate key index: $DUPLICATES"
fi

# Restore default "configuration/keys.db"
#
mv ${CONFIGURATION_KEY_FILENAME}_default $CONFIGURATION_KEY_FILENAME
