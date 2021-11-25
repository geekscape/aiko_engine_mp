#!/bin/sh
#
# To Do
# ~~~~~
# - None, yet !

MANIFEST=manifest
UPGRADE_TOPIC=upgrade/aiko_00
VERSION=v05
RELEASE_PATHNAME=aiko_$VERSION
rm -rf $RELEASE_PATHNAME

mkdir $RELEASE_PATHNAME
mkdir $RELEASE_PATHNAME/applications
mkdir $RELEASE_PATHNAME/applications/schedule
mkdir $RELEASE_PATHNAME/configuration
mkdir $RELEASE_PATHNAME/examples
mkdir $RELEASE_PATHNAME/lib
mkdir $RELEASE_PATHNAME/lib/aiko
mkdir $RELEASE_PATHNAME/plugins

cp applications/default.py     $RELEASE_PATHNAME/applications
cp applications/schedule/schedule.py  $RELEASE_PATHNAME/applications/schedule
cp applications/swagbadge.py   $RELEASE_PATHNAME/applications

cp configuration/main.py       $RELEASE_PATHNAME/configuration
cp configuration/led.py        $RELEASE_PATHNAME/configuration
cp configuration/mqtt.py       $RELEASE_PATHNAME/configuration
# cp configuration/net.py      $RELEASE_PATHNAME/configuration
cp configuration/oled.py       $RELEASE_PATHNAME/configuration
cp configuration/schedule.py   $RELEASE_PATHNAME/configuration
cp configuration/services.py   $RELEASE_PATHNAME/configuration
cp configuration/system_ui.py  $RELEASE_PATHNAME/configuration

cp lib/aiko/button.py          $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/common.py          $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/event.py           $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/led.py             $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/mqtt.py            $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/net.py             $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/oled.py            $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/queue.py           $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/services.py        $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/system_ui.py       $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/test.py            $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/upgrade.py         $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/web_client.py      $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/web_server.py      $RELEASE_PATHNAME/lib/aiko

cp lib/ili9341.py              $RELEASE_PATHNAME/lib
cp lib/mpu9250.py              $RELEASE_PATHNAME/lib
cp lib/shutil.py               $RELEASE_PATHNAME/lib
cp lib/ssd1306.py              $RELEASE_PATHNAME/lib
cp lib/threading.py            $RELEASE_PATHNAME/lib

cp plugins/__init__.py         $RELEASE_PATHNAME/plugins

cp main.py                     $RELEASE_PATHNAME

find $RELEASE_PATHNAME -type f \( -exec md5sum {} \; -exec wc -c {} \; \) | paste - - | column -t | tr -s "[:blank:]" | cut -d" " -f1,3,4 | sort -k 3 >$MANIFEST
mv $MANIFEST $RELEASE_PATHNAME/$MANIFEST
chmod -R 755 $RELEASE_PATHNAME
find $RELEASE_PATHNAME -type f -exec chmod 444 '{}' \;
tar -cf $RELEASE_PATHNAME.tar $RELEASE_PATHNAME

FILE_COUNT=`wc -l $RELEASE_PATHNAME/$MANIFEST | column -t | cut -d" " -f 1`
MANIFEST_CHECKSUM=`md5sum $RELEASE_PATHNAME/$MANIFEST | column -t | cut -d" " -f1`
MANIFEST_SIZE=`wc -c $RELEASE_PATHNAME/$MANIFEST | column -t | cut -d" " -f1`
URL=http://209.141.52.199:8888/$RELEASE_PATHNAME/$MANIFEST
QUOTE=\'

echo '### FIRMWARE DETAILS --> MOSQUITTO UPGRADE TOPIC ###'
echo 'mosquitto_pub -u ?????? -P ?????? -h lounge.local -t '$UPGRADE_TOPIC' -r -m '$QUOTE'('upgrade $VERSION $URL $MANIFEST_CHECKSUM $MANIFEST_SIZE $FILE_COUNT')'$QUOTE
rm -rf $RELEASE_PATHNAME
