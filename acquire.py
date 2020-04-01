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
import matplotlib.pyplot as plt
from pymodbus.client.sync import ModbusSerialClient

import bme280 as bme
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
        data=np.full((10000, 8), '', dtype=object),
        columns=['date',
                 'time_min',
                 'voltage_v',
                 'current_amps',
                 'power_watts',
                 'temp_c',
                 'press_atm',
                 'rh_%'])
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
ps = hps.open_ps('/dev/ttyUSB0')
hps.output_on(ps)

'''
# specify power supply settings
settings = np.column_stack(
    (np.linspace(0, 10, 10),
     np.full(10, 0.2)))
'''

# set power supply output
hps.set_output(ps, voltage=12, current=4)

step_duration = 3
minutes_elapsed = 0

row_counter = 0
while minutes_elapsed < step_duration:  

    # read current time
    current_time, minutes_elapsed = get_times(start_time)
    # read barometric data
    bme_output = list(bme.read_all())
    bme_output[2] /= 100
    print(bme_output)
    # read voltage, current, power output of power supply
    ps_output = hps.read_output(ps)

    # append data to log
    df.iloc[row_counter] = [current_time, minutes_elapsed, *ps_output, *bme_output]

    row_counter += 1
    time.sleep(2)
    

# close power supply
hps.close_ps(ps)

df.dropna().to_csv(logpath, index=False)


plt.plot(pd.to_numeric(df['time_min']), pd.to_numeric(df['temp_c']))
plt.show()
