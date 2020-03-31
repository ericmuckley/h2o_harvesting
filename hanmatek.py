"""
This module provides methods for controlling the
Hanmatek HM310P DC power supply.

Created on: March 30, 2020
Author: ericmuckley@gmail.com
"""

import time
import serial
from serial.tools import list_ports
from pymodbus.client.sync import ModbusSerialClient

def print_ports():
    """Print a list of avilable serial ports."""
    ports = list(list_ports.comports())
    print('Available serial ports:')
    [print(p.device) for p in ports]

def open_ps(port):
    """Open connection to Hanmatek HM310P DC power supply."""
    dev = ModbusSerialClient(
        method="rtu",
        port=port,
        stopbits=1,
        bytesize=8,
        parity="N",
        baudrate=9600,
        timeout=0.5)
    connection = dev.connect()
    if not connection:
        print("Connection to HM310P failed.")
    else:
        print("HM310P connected")
    return dev

def close_ps(dev):
    """Close connection to Hanmatek HM310P DC power supply."""
    try:
        dev.output_off()
        dev.close()
        print("HM310P closed.")
    except AttributeError:
        print("HM310P could not close.")


def output_on(dev):
    """Turn on output of Hanmatek HM310P DC power supply."""
    try:
        dev.write_register(address=int('1', 16), count=1, value=1, unit=1)
    except AttributeError:
        print("Could not turn output on.")

def output_off(dev):
    """Turn off output of Hanmatek HM310P DC power supply."""
    try:
        dev.write_register(address=int('1', 16), count=1, value=0, unit=1)
    except AttributeError:
        print("Could not turn output off.")

def set_voltage(dev, voltage):
    """Set voltage level of Hanmatek HM310P DC power supply."""
    try:
        voltage_int = int(round(float(voltage)*100, 2))
        dev.write_register(address=int('30', 16),
                           count=1,
                           value=voltage_int,
                           unit=1)
    except AttributeError:
        print("could not set voltage.")

def set_current(dev, current):
    """Set current level of Hanmatek HM310P DC power supply."""
    try:
        current_int = int(round(float(current)*1000, 2))
        device.write_register(address=int('31', 16),
                              count=1,
                              value=current_int,
                              unit=1)
    except AttributeError:
        print("could not set current.")

def read_output_levels(dev):
    """Read output levelsof the Hanmatek HM310P DC power supply."""
    r = device.read_holding_registers(address=16, count=4, unit=1)
    voltage = float(r.registers[0]) / 100
    current = float(r.registers[1]) / 1000
    power = (float(r.registers[2]) + float(r.registers[3])) / 1000
    return (voltage, current, power)
        

if __name__ == '__main__':
    print_ports()

    ps = open_ps('COM3')
    time.sleep(2)
    output_on(ps)
    time.sleep(2)

    set_voltage(dev, 3)
    set_current(dev, 1)


    time.sleep(2)
    levels = read_outout_levels(dev)
    print(levels)

    time.sleep(1)


    output_off(ps)
    time.sleep(2)
    close_ps(ps)
