import re

from .tty_serial import *
# from ..instruments.iq_flex_5g import IQView

class DutSiA28(DutProtocol):
    def __init__(self):
        super(DutSiA28, self).__init__()
        self._init_ok = False
        
    def _event_cb_default(self, line=""):
        if re.search("", line):
            self._init_ok = True
            
    def set_init_ok(self, line):
        logger.info("init ok")
        self._init_ok = True
        return True

    def cali_init(self):
        logger.debug("command ls ...")
        self.re_set_exp('read all_power or save_all power', self.set_init_ok)
        self.command("ate_init")
        return super(DutSiA28, self).cali_init()
    
    def cali_quit(self):
        logger.debug("cali quit")
        
    def cali_auto_complite(self, iq):
        logger.info("process calibration...")
        iq.GetEVM()
        return True

class DutSiFlowers(object):
    def __init__(self, tty="/dev/ttyUSB0", baudrate=115200, bytesize=8, parity="N", stopbits=1):
        self.ser = serial.Serial(tty, baudrate, bytesize, parity, stopbits)
        self.quit = False
        logger.info("contstructor inited")
        
    def quit_cali(self):
        logger.info("quit running cali")
        self.quit = True
        
    def auto_cali(self, iq):
        with serial.threaded.ReaderThread(self.ser, DutSiA28) as dut:
            self.dut = dut
            logger.debug("reset ...")
            dut.reset()
            dut.cali_init()
            iq.InitInst()
            while self.quit == False:
                dut.cali_auto_complite(iq)
                pass
                
