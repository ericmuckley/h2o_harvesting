"""
This module provides methods for controlling the
Hanmatek HM310P DC power supply and ....

Created on: March 31, 2020
Author: ericmuckley@gmail.com
"""

import os
import time
import numpy as np
import pandas as pd
from serial.tools import list_ports
from pymodbus.client.sync import ModbusSerialClient

import hanmatek as hps


def create_data_log():
    """Create folder and Pandas dataframe for logging data."""
    # create directory for logging data
    logdir = os.path.join(os.getcwd(), 'log')
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    # create filename for logging data
    starttime = time.strftime('%Y-%m-%d_%H-%M-%S')
    logpath = os.path.join(logdir, starttime+'__log.csv')
    # create dataframe for storing data
    df = pd.DataFrame(
        data=np.full((10000, 5), '', dtype=object),
        columns=['date',
                 'minutes_elapsed',
                 'volts',
                 'amps',
                 'watts'])
    return logpath, df


def get_times(start_time):
    """Get current date/time and elapsed time."""
    current_time = time.strftime('%Y-%m-%d_%H-%M-%S')
    minutes_elapsed = round((time.time() - start_time)/60, 2)
    return current_time, minutes_elapsed


# create log file
start_time = time.time()
logpath, df = create_data_log()

# open connection to power supply
ps = hps.open_ps("COM3")
hps.output_on(ps)

# specify power supply settings
settings = np.column_stack(
    (np.linspace(0, 10, 10),
     np.full(10, 0.2)))


for s in range(len(settings)):

    # set power supply output
    hps.set_output(ps, voltage=settings[s, 0], current=settings[s, 1])

    # read voltage, current, power output of power supply
    output = hps.read_output(ps)
    # read current time
    current_time, minutes_elapsed = get_times(start_time)
    # append data to log
    df.iloc[s] = [current_time, minutes_elapsed, *output]

    time.sleep(3)

# close power supply
hps.close_ps(ps)

df.dropna().to_csv(logpath, index=False)
