
from .si_a28 import DutSiFlowers

def __name__():
    si28 = DutSiFlowers(tty="/dev/ttyUSB2")
    si28.auto_cali()