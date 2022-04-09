import os
import glob
import time
import MySQLdb
import datetime
import sys
import read_weight

# Set read delay time
delay_sec = 600

# Set DB configuration
host = "localhost"
user = "sensordev"
passwd = user
db_name = user
db = MySQLdb.connect(host, user, passwd, db_name)
cur=db.cursor()

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
    print '\n' + '==========' + '\nClosing database connection...'
    cur.close()
    db.close()
    print 'Sensor read stopped at ' + str(ttime.strftime("%X")) + '\n=========='
    sys.exit()

while True:
    try:
        time.sleep(delay_sec)
    except (KeyboardInterrupt, SystemExit):
        sys.exit()

    # Set cycle date and time
    tdatetime=datetime.datetime.now()
    ttime=datetime.datetime.now().time()

    # Read and write weight
    try:
        weight=read_weight.read_weight()
        weight_query = "INSERT INTO hive (sensorID, tdatetime, data) VALUES (%s,%s,%s)"

        # Hard code weight sensor as sensor 0
        weight_args = (0,tdatetime,weight)
        cur.execute(weight_query, weight_args)
        db.commit()
    except (KeyboardInterrupt, SystemExit):
        db.rollback()
        exitProgram()
    except:
        db.rollback()
        print 'Encountered a weight write error at ' + str(ttime.strftime("%X"))

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
                query = "INSERT INTO hive (sensorID, tdatetime, data) VALUES (%s,%s,%s)"
                args = (sensornum+1,tdatetime,temp)
                cur.execute(query, args)
                db.commit()
            except (KeyboardInterrupt, SystemExit):
                exitProgram()
            except:
                db.rollback()
                print 'Encountered a temp write error at ' + str(ttime.strftime("%X"))
        print('Data written at ' + str(ttime.strftime("%X")) + '.')
    except (KeyboardInterrupt, SystemExit):
        db.rollback()
        exitProgram()
    except:
        db.rollback()
        print 'Encountered a temp write error at ' + str(ttime.strftime("%X"))
