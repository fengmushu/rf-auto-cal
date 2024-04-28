#!/usr/bin/env python3

import time
import signal
import logging
logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s %(message)s", filename="dut.log", level=logging.INFO)

from dut.si_a28 import DutSiFlowers
from instruments.iq_flex_5g import IQView

def handler(signum, frame):
    print("Sig handle: {}, quit()".format(signum))
    sia28.Quit()
    exit(0)

# signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)

# DEFINE
TTY_USB="/dev/ttyUSB0"
IQ_URL="http://192.168.10.254"
DIR_REPORTS="./reports"

# main process of calibration
sia28 = DutSiFlowers(tty=TTY_USB)
IQ = IQView(URL=IQ_URL)
def cali_process(dut, proto):
    # dut is <sia28>
    proto.Reset()
    # proto.Init()
    IQ.InitIQ()
    IQ.SetSettings()
    IQ.SetHardware()
    while dut.Running():
        IQ.SetHardware(freq=2412)
        proto.SetRadio(freq=2412, bw=20, mcs=7)
        IQ.GetPowerEVM(retry=10)
        time.sleep(10)
        pass
    IQ.Quit()
    pass

sia28.AutoCali(cali_process)
