import struct
import math

class MPU9250:
    """support for the MPU-9250"""

    FS_2G = 0
    FS_4G = 8
    FS_8G = 16
    FS_16G = 24

    def __init__(self, bus, accel_max_g=2, addr=104):
        self.bus = bus
        self.addr = addr
        if accel_max_g <= 2: 
            accel_fs_sel = 0
            self.accel_scale = 16384
        elif accel_max_g <= 4:
            accel_fs_sel = 8
            self.accel_scale = 8192
        elif accel_max_g <= 8:
            accel_fs_sel = 16
            self.accel_scale = 4096
        elif accel_max_g <= 16:
            accel_fs_sel = 24
            self.accel_scale = 2048
        else:
            raise ValueError("accel_max_g must be <= 16")

        self.bus.writeto_mem(self.addr, 107, bytes([0]))
        self.bus.writeto_mem(self.addr, 28, bytes([accel_fs_sel]))

    def read(self):
        (ax, ay, az, _, gx, gy, gz) = struct.unpack(">7h", self.bus.readfrom_mem(104,0x3b,14))
        #return math.sqrt(ax*ax + ay*ay + az*az) / self.accel_scale, math.sqrt(gx*gx + gy*gy + gz*gz)
        return az / self.accel_scale, gz

