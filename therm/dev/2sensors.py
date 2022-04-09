# This file is used to print the temperature sensor readings from two sensors

import os
import glob
import time
import datetime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
sensor0_folder = glob.glob(base_dir + '28*')[0]
sensor0_file = sensor0_folder + '/w1_slave'

sensor1_folder = glob.glob(base_dir + '28*')[1]
sensor1_file = sensor1_folder + '/w1_slave'

def read_temp_raw0():
    f = open(sensor0_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp0():
    lines = read_temp_raw0()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw0()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

def read_temp_raw1():
    f = open(sensor1_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp1():
    lines = read_temp_raw1()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw1()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

while True:
    print("\n\n\n\n\n\n\n===================================")
    print(datetime.datetime.now())
    print("\n Probe 0:")
    print(read_temp0())
    print("\n Probe 1:")
    print(read_temp1())
    time.sleep(1)
