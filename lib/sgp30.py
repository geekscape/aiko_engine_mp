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

    def __init__(self, i2c, address=__SGP30_DEFAULT_I2C_ADDR):
        self._device = i2c
        self.address = address
        self.serial = self._i2c_read_words_from_cmd(
                [self.__SGP30_SERIAL_HIGH, self.__SGP30_SERIAL_LOW], 0.01, 3)

        # get featuerset
        featureset = self._i2c_read_words_from_cmd(
            [self.__SGP30_CMD_HIGH, 0x2f], 0.01, 1)

        if featureset[0] != self.__SGP30_FEATURESET:
            raise RuntimeError('SGP30 Not detected')
        self.iaq_init()


    @property
    def tvoc(self):
        """Total Volatile Organic Compound in parts per billion."""
        return self.iaq_measure()[1]


    @property
    def baseline_tvoc(self):
        """Total Volatile Organic Compound baseline value"""
        return self.get_iaq_baseline()[1]


    @property
    def co2eq(self):
        """Carbon Dioxide Equivalent in parts per million"""
        return self.iaq_measure()[0]


    @property
    def baseline_co2eq(self):
        """Carbon Dioxide Equivalent baseline value"""
        return self.get_iaq_baseline()[0]


    def iaq_init(self):
        """Initialize the IAQ algorithm"""
        # name, command, signals, delay
        self._run_profile(["iaq_init", [self.__SGP30_CMD_HIGH, 0x03], 0, 0.01])

    def iaq_measure(self):
        """Measure the CO2eq and TVOC"""
        # name, command, signals, delay
        return self._run_profile(["iaq_measure", 
                [self.__SGP30_CMD_HIGH, 0x08], 2, 0.05])

    def get_iaq_baseline(self):
        """Retreive the IAQ algorithm baseline for CO2eq and TVOC"""
        # name, command, signals, delay
        return self._run_profile(["iaq_get_baseline", 
                [self.__SGP30_CMD_HIGH, 0x15], 2, 0.01])


    def set_iaq_baseline(self, co2eq, tvoc):
        """Set the previously recorded IAQ algorithm baseline for CO2eq and TVOC"""
        if co2eq == 0 and tvoc == 0:
            raise RuntimeError('Invalid baseline')
        buffer = []
        for value in [tvoc, co2eq]:
            arr = [value >> 8, value & 0xFF]
            arr.append(self._generate_crc(arr))
            buffer += arr
        self._run_profile(["iaq_set_baseline", 
            [self.__SGP30_CMD_HIGH, 0x1e] + buffer, 0, 0.01])


    # Low level command functions

    def _run_profile(self, profile):
        """Run an SGP 'profile' which is a named command set"""
        # pylint: disable=unused-variable
        name, command, signals, delay = profile
        # pylint: enable=unused-variable

        print("\trunning profile: %s, command %s, %d, delay %0.02f" %
           (name, ["0x%02x" % i for i in command], signals, delay))
        return self._i2c_read_words_from_cmd(command, delay, signals)


    def _i2c_read_words_from_cmd(self, command, delay, reply_size):
        """Run an SGP command query, get a reply and CRC results if necessary"""
        #with self._device:
        print("\tAddress: " +  str(self.address) + " Command: " + str(bytes(command)))
        self._device.writeto(self.address, bytes(command))
        time.sleep(delay)
        if not reply_size:
            return None
        crc_result = bytearray(reply_size * (self.__SGP30_WORD_LEN +1))
        self._device.readinto(crc_result)
        print("\tRaw Read: ", crc_result)
        result = []
        for i in range(reply_size):
            word = [crc_result[3*i], crc_result[3*i+1]]
            crc = crc_result[3*i+2]
            if self._generate_crc(word) != crc:
                raise RuntimeError('CRC Error')
            result.append(word[0] << 8 | word[1])
        print("\tOK Data: ", [hex(i) for i in result])
        return result


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