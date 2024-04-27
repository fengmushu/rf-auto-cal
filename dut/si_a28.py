from .tty_serial import *

class DutProtocolSi(DutProtocol):
    def __init__(self):
        super(DutProtocolSi, self).__init__()

    # def cal_init(self):
    #     return super(DutProtocolSi, self).cal_init()

class DutSiFlowers(object):
    def __init__(self, tty="/dev/ttyUSB0", baudrate=115200, bytesize=8, parity="N", stopbits=1):
        self.ser = serial.Serial(tty, baudrate, bytesize, parity, stopbits)
        logger.info("contstructor inited")
        
    def auto_cali(self):
        with serial.threaded.ReaderThread(self.ser, DutProtocolSi) as dut:
            self.dut = dut
            dut.reset()

# def main():
#     dut = DutSiFlowers()
#     dut.auto_cali()
# main()