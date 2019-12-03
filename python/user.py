#!/usr/bin/python3
# -*-coding:utf-8 -*

import serial
import serial.tools.list_ports
from time import sleep
import numpy as np
import atexit

serial_ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    if 'Nucleo' in p.description
]
if not serial_ports:
    raise IOError("No nucleo found")
if len(serial_ports) > 1:
    raise IOError('Multiple nucleos found')


def exit_handler():
    """A basic exit handler that tells the arduino
    to stop the driver when program is exited

    It actually exploits the fact that the program
    restarts when you connect to the arduino.
    """

    with serial.Serial(serial_ports[0], 9600, timeout=3.0) as nucleo:
        print('terminating')


atexit.register(exit_handler)


def write_message(target, message, verbose=False):
    if type(message) is str:
        if verbose:
            print('You are sending "' + message + '" to the target')
        message = message + '\n'
        message = message.encode('utf-8')
    if type(message) is bytes:
        if verbose:
            print('You are sending "' + message.decode('utf-8') + '" to the target')

    target.write(message)
    return message


with serial.Serial(serial_ports[0], 9600, timeout=2) as nucleo:

    sleep(1)
    print('Serial is open: {}'.format(nucleo.is_open))
    while True:

        in_str = input('Input command string or q to quit :').lower()
        if in_str == 'q':
            break
        else:
            write_message(nucleo, in_str, verbose=True)
        print(nucleo.readline().decode('utf-8'))
