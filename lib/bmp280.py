import struct
import time
import math

class BMP280:
    """Support for the Bosch BMP280 atmospheric temperature/pressure sensor"""

    def __init__(self, bus, addr=118):
        self.bus = bus
        self.addr = addr

        self.bus.writeto_mem(self.addr, 0xE0, bytes([0xB6]))
        time.sleep(0.1)
        assert(self.bus.readfrom_mem(self.addr, 0xD0, 1) == b'\x58')

        self.bus.writeto_mem(self.addr, 0xF4, bytes([0x3F]))
        self.trim = struct.unpack("<HhhHhhhhhhhh", self.bus.readfrom_mem(self.addr, 0x88, 24))

    def read(self):
        (up, upx, ut, utx) = struct.unpack(">HBHB", self.bus.readfrom_mem(self.addr, 0xF7, 6))

        # 20 bit values for raw temperature and pressure
        up = (up << 4) + (upx >> 4)
        ut = (ut << 4) + (utx >> 4)

        # Based on the BMP280 Datasheet Appendix 8.1: Floating Point implementation
        # This is not easy to follow!

        dt1, dt2, dt3, dp1, dp2, dp3, dp4, dp5, dp6, dp7, dp8, dp9 = self.trim

        v1 = ((ut / 16384.0) - (dt1 / 1024.0)) * dt2
        v2 = ((ut / 131072.0) - (dt1 / 8192.0))**2 * dt3
        t_fine = v1 + v2
        t = t_fine / 5120

        v1 = (t_fine/2.0) - 64000.0
        v2 = v1 * v1 * dp6 / 32768.0
        v2 = v2 + (v1 * dp5 * 2.0)
        v2 = (v2 / 4.0) + (dp4 * 65536.0)
        v1 = (dp3 * v1 * v1 / 524288.0 + (dp2 * v1)) / 524288.0
        v1 = (1 + v1 / 32768.0) * dp1

        if v1 == 0: return t, None, None

        p = 1048576.0 - up
        p = (p - (v2 / 4096.0)) * 6250.0 / v1
        v1 = dp9 * p * p / 2147483648.0
        v2 = p * dp8 / 32768.0
        p = p + (v1 + v2 + dp7) / 16.0

        # Altitude estimate from hypsometric formula
        h = (1 - math.pow((p / 101325), 1/5.257)) * (t + 273.15) / 0.0065
        return t, p, h

