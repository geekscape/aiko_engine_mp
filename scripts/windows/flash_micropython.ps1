
if ([string]::IsNullOrEmpty($env:AMPY_PORT)) {
    $env:AMPY_PORT = 'COM9'
}

if ([string]::IsNullOrEmpty($env:BAUDRATE)) {
    $env:BAUDRATE = '460800'
}

if ([string]::IsNullOrEmpty($env:ESP32_MICROPYTHON)) {
    $env:ESP32_MICROPYTHON = './esp32-idf4-20191220-v1.12.bin'
}


echo "### Erase flash ###"
py $env:VIRTUAL_ENV\Scripts\esptool.py-script.py --chip esp32 --port $env:AMPY_PORT erase_flash

echo "### Flash microPython ###"
py $env:VIRTUAL_ENV\Scripts\esptool.py-script.py --chip esp32 --port $env:AMPY_PORT --baud $env:BAUDRATE write_flash -z 0x1000 $env:ESP32_MICROPYTHON

echo "### Complete ###"
