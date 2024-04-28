#!/usr/bin/env python3

import signal
import logging
logging.basicConfig(format="%(asctime)s %(module)s %(name)s %(message)s", filename="dut.log", level=logging.NOTSET)

from dut.si_a28 import DutSiFlowers
from instruments.iq_flex_5g import IQView

def handler(signum, frame):
    print("Sig handle: {}, quit()".format(signum))
    sia28.quit_cali()
    exit(0)

# signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)

# main process of calibration
sia28 = DutSiFlowers(tty="/dev/ttyUSB2")
sia28.auto_cali(IQView(URL="http://192.168.10.254"))
