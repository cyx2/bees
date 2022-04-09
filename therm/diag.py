import os
import glob
import time
import MySQLdb
import datetime
import sys
import read_weight

# Set read delay time
delay_sec = 0

# Retrieves lines from sensor readout file
def read_temp_raw(sensor):
    temp_sensor_dir = sensor_dir[sensor] + sensor_file_tail
    f = open(temp_sensor_dir, 'r')
    lines = f.readlines()
    f.close()
    return lines

# Returns farenheit temperature measurements
def read_temp(sensor):
    lines = read_temp_raw(sensor)
    while lines[0].strip()[-3:] != 'YES':
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

def exitProgram():
    print '\nDiagnostic tool stopped at: ' + str(ttime.strftime("%X"))
    sys.exit()

while True:
    # Set cycle date and time
    tdate=datetime.datetime.now().date()
    ttime=datetime.datetime.now().time()

    print '\n============== ' + str(ttime.strftime("%X")) + ' =============='

    try:
        time.sleep(delay_sec)
    except (KeyboardInterrupt, SystemExit):
        sys.exit()

    # Read and write weight
    try:
        weight=read_weight.read_weight()

        print 'Weight sensor reads ' + str(weight)
    except (KeyboardInterrupt, SystemExit):
        exitProgram()
    except:
        print 'Encountered a weight read error at ' + str(ttime.strftime("%X"))

    # Read and write temperature
    try:
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        # Get directories for therm probes
        sensor_dir = glob.glob('/sys/bus/w1/devices/' + '28*')
        sensor_dir_len = len(sensor_dir)
        sensor_file_tail = '/w1_slave'
        print('** Acquired ' + str(sensor_dir_len) + ' temp sensor(s) **')

        # Iterate through temperature sensors
        for sensornum in range(0,sensor_dir_len):
            temp=read_temp(sensornum)
            try:
                print 'Sensor ' + str(sensornum) + ' reads ' + str(temp)
            except (KeyboardInterrupt, SystemExit):
                exitProgram()
            except:
                print 'Encountered a temp print error at ' + str(ttime.strftime("%X"))
    except (KeyboardInterrupt, SystemExit):
        exitProgram()
    except:
        print 'Encountered a temp read error at ' + str(ttime.strftime("%X"))
