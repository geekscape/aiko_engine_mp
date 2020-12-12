#!/bin/sh
#
# To Do
# ~~~~~
# - None, yet !

RELEASE_PATHNAME=aiko_v03
rm -rf $RELEASE_PATHNAME

mkdir $RELEASE_PATHNAME
mkdir $RELEASE_PATHNAME/applications
mkdir $RELEASE_PATHNAME/configuration
mkdir $RELEASE_PATHNAME/examples
mkdir $RELEASE_PATHNAME/lib
mkdir $RELEASE_PATHNAME/lib/aiko

cp applications/default.py    $RELEASE_PATHNAME/applications
cp applications/swagbadge.py  $RELEASE_PATHNAME/applications

cp configuration/main.py      $RELEASE_PATHNAME/configuration
cp configuration/led.py       $RELEASE_PATHNAME/configuration
cp configuration/mqtt.py      $RELEASE_PATHNAME/configuration
# cp configuration/net.py     $RELEASE_PATHNAME/configuration
cp configuration/oled.py      $RELEASE_PATHNAME/configuration
cp configuration/services.py  $RELEASE_PATHNAME/configuration

cp lib/aiko/common.py         $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/event.py          $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/led.py            $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/mqtt.py           $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/net.py            $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/oled.py           $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/queue.py          $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/services.py       $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/test.py           $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/upgrade.py        $RELEASE_PATHNAME/lib/aiko
cp lib/aiko/web_server.py     $RELEASE_PATHNAME/lib/aiko

cp lib/mpu9250.py             $RELEASE_PATHNAME/lib
cp lib/shutil.py              $RELEASE_PATHNAME/lib
cp lib/ssd1306.py             $RELEASE_PATHNAME/lib
cp lib/threading.py           $RELEASE_PATHNAME/lib
cp lib/utarfile.py            $RELEASE_PATHNAME/lib

tar -cf $RELEASE_PATHNAME.tar $RELEASE_PATHNAME
rm -rf $RELEASE_PATHNAME
