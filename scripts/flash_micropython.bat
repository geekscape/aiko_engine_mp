set AMPY_PORT=COM9
set BAUDRATE=460800
set ESP32_MICROPYTHON=firmware/esp32-20180602-v1.9.4-113-g7d86ac6c.bin

echo "### Erase flash ###"
esptool --chip esp32 --port %AMPY_PORT% erase_flash

echo "### Flash microPython ###"
esptool --chip esp32 --port %AMPY_PORT% --baud %BAUDRATE% write_flash -z 0x1000 %ESP32_MICROPYTHON%

echo "### Complete ###"
