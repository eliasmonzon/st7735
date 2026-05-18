from machine import Pin, SPI
import time

_CMD_TIMEOUT = const(100)

class SDCard:
    def __init__(self, spi, cs):
        self.spi = spi
        self.cs = cs
        self.cs.init(Pin.OUT, value=1)
        self.init_card()

    def init_spi(self):
        self.cs.value(1)
        for i in range(16):
            self.spi.write(b"\xff")

    def cmd(self, cmd, arg, crc, final=0, release=True):
        self.cs.value(0)
        buf = bytearray(6)
        buf[0] = 0x40 | cmd
        buf[1] = (arg >> 24) & 0xff
        buf[2] = (arg >> 16) & 0xff
        buf[3] = (arg >> 8) & 0xff
        buf[4] = arg & 0xff
        buf[5] = crc
        self.spi.write(buf)
        
        for i in range(_CMD_TIMEOUT):
            response = self.spi.read(1, 0xff)[0]
            if not (response & 0x80):
                if final:
                    self.spi.read(final, 0xff)
                if release:
                    self.cs.value(1)
                    self.spi.write(b"\xff")
                return response
        self.cs.value(1)
        self.spi.write(b"\xff")
        return -1

    def init_card(self):
        self.init_spi()
        for i in range(5):
            if self.cmd(0, 0, 0x95) == 1:
                break
        else:
            raise OSError("No SD card")
        
        while True:
            self.cmd(55, 0, 0)
            if self.cmd(41, 0x40000000, 0) == 0:
                break
        print("SD inicializada")

    def readblocks(self, block_num, buf):
        self.cmd(17, block_num * 512, 0, release=False)
        while True:
            token = self.spi.read(1, 0xff)[0]
            if token == 0xFE:
                break
        self.spi.readinto(buf)
        self.spi.read(2, 0xff)
        self.cs.value(1)
        self.spi.write(b"\xff")

    def writeblocks(self, block_num, buf):
        self.cmd(24, block_num * 512, 0, release=False)
        self.spi.write(b"\xfe")
        self.spi.write(buf)
        self.spi.write(b"\xff\xff")
        response = self.spi.read(1, 0xff)[0]
        if (response & 0x1f) != 0x05:
            self.cs.value(1)
            raise OSError("SD write error")
        while self.spi.read(1, 0xff)[0] == 0:
            pass
        self.cs.value(1)
        self.spi.write(b"\xff")

    def ioctl(self, op, arg):
        if op == 4:   # get number of blocks
            return 32768
        if op == 5:   # get block size
            return 512
        if op == 6:   # sync
            return 0