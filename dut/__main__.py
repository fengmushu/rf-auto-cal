
from .tty_serial import DutSiFlowers

def main():
    dut = DutSiFlowers()
    dut.auto_cali()
main()