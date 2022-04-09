import os
import glob
import time

# Refresh probe list
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Therm probe system directory
sensor_dir = glob.glob('/sys/bus/w1/devices/' + '28*')
sensor_dir_len = len(sensor_dir)
sensor_file_tail = '/w1_slave'
print('Acquired ' + str(sensor_dir_len) + ' sensor(s)')

# Retrieves lines from sensor readout file
def read_temp_raw(sensor):
    temp_sensor_dir = sensor_dir[sensor] + sensor_file_tail
    f = open(temp_sensor_dir, 'r')
    lines = f.readlines()
    f.close()
    return lines

# Returns celsius and farenheit temperature measurements
def read_temp(sensor):
    lines = read_temp_raw(sensor)
    print('Reading sensor ' + str(sensor+1))
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

while True:
    time.sleep(3)
    print("\n===================================")
    print('Attemping to print data for ' + str(sensor_dir_len) + ' sensor(s)')
    for sensornum in range(0,sensor_dir_len):
        print(read_temp(sensornum))
