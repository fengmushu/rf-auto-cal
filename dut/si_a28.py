import re

from .tty_serial import *

class DutSiA28(DutProtocol):
    def __init__(self):
        super(DutSiA28, self).__init__()
        self.__status = 'idle'
        
    def __fsm_update(self, line, args=[]):
        self.__status = args[0]
        return True

    def Init(self):
        logger.debug("command ls ...")
        self.ReSetExp('read all_power or save_all power', self.__fsm_update, ['init'])
        self.Command("ate_init")
        return super(DutSiA28, self).Init()
    
    def SetRadio(self, freq=2412, bw=20, mcs=7):
        pass

class DutSiFlowers(object):
    def __init__(self, tty="/dev/ttyUSB0", baudrate=115200, bytesize=8, parity="N", stopbits=1):
        self.ser = serial.Serial(tty, baudrate, bytesize, parity, stopbits)
        self._running = True
        logger.info("init")

    def AutoCali(self, cali_process):
        with serial.threaded.ReaderThread(self.ser, DutSiA28) as proto:
            cali_process(self, proto)

    def Running(self):
        return self._running

    def Quit(self):
        self._running = False
        logger.info("quit...")
        pass
