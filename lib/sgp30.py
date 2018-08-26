import struct
import time
import math

class SGP30:
    __SGP30_DEFAULT_I2C_ADDR  = 0x58
    __SGP30_FEATURESET        = 0x0020

    __SGP30_CRC8_POLYNOMIAL   = 0x31
    __SGP30_CRC8_INIT         = 0xFF
    __SGP30_WORD_LEN          = 2

    __SGP30_SERIAL_HIGH      = 0x36
    __SGP30_SERIAL_LOW      = 0x82

    __SGP30_CMD_HIGH         = 0x20


    def __init__(self, i2c, address=__SGP30_DEFAULT_I2C_ADDR)
        self._device = i2c
        self.address = address

        self.serial = self._device.






    def _generate_crc(self, data):
        """8-bit CRC algorithm for checking data"""
        crc = self.__SGP30_CRC8_INIT
        # calculates 8-Bit checksum with given polynomial
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ self.__SGP30_CRC8_POLYNOMIAL
                else:
                    crc <<= 1
        return crc & 0xFF