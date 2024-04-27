#!/usr/bin/env python3

from dut.tty_serial import DutSiFlowers

def main():
    with DutSiFlowers() as dut:
        dut.reset()
        print("reset...")
        # dut.command("ls /tmp")
main()