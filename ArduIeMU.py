'''
IMU data emulator
Daniel Compton

'''
import serial
import struct
import time
import sys
from multiprocessing import Process


class ArduIeMU(object):

    def __init__(self, port,baud):
        self.ser = serial.Serial(port, baud)
        self.pream = 'DIYd'

    def loop(self):
        data = []
        # Loop and read all of the data from the IMU
        while 1:
            buff = self.ser.read(1)
            if buff == self.pream[0]:
                # got the pream, read the next 3 bytes
                buff = self.ser.read(3)
                if buff[0] == 'I' and buff[1] == 'Y' and buff[2] == 'd':
                    buff = self.ser.read(2) # skip the checksum and what not
                    x = struct.unpack("bb",buff)
                    if ord(buff[1]) == 0x02:
                        x = self.readRPY()
                        if len(data) > 1000:
                            data = data[500:1000]
                        data.append(list(x))
                    else:
                        print x

                    if ord(buff[1]) == 0x03:
                        print buff
                        print self.readGPS()

    def doCheckSum(self, buff, ck):
        # Calculate checksums
        IMU_ck_a = 0
        IMU_ck_b = 0
        for i in range(0, ck+2):
            IMU_ck_a = IMU_ck_a + ord(buff[i])
            IMU_ck_b = IMU_ck_b + IMU_ck_a

        # print to the serial interface
        self.ser.write(IMU_ck_a)
        self.ser.write(IMU_ck_b)

    def readRPY(self):
        '''
        roll pitch and yaw data are stored in a 6 byte struct
        [low_roll, high_roll, low_pitch, high_pitch, low_yaw, high_yaw]
        '''
        if False:
            data = self.ser.read(6)
            roll,pitch,yaw = struct.unpack('<hhh', data)
            roll = roll/100
            pitch = pitch/100
            yaw = yaw/100

        #if False:
        # Get roll
        data = self.ser.read(6)
        roll,pitch,yaw = struct.unpack("<hhh",data)
        tmp = [roll,pitch,yaw]
        print tmp

        return tmp

    def sendRPY(self,roll,pitch,yaw):
        '''
        roll pitch and yaw data are stored in a 6 byte struct
        [low_roll, high_roll, low_pitch, high_pitch, low_yaw, high_yaw]
        specfied in degrees*100
        '''
        self.ser.write('DIYd')
        buff = [0x06,0x02]
        ck=6
        # pack the roll
        roll = roll * 100
        temp = struct.pack('<h', roll)
        buff.extend(temp)

        # pack the pitch
        pitch = pitch * 100
        temp = struct.pack('<h', pitch)
        buff.extend(temp)

        # pack the yaw
        yaw = yaw * 100
        temp = struct.pack('<h', yaw)
        buff.extend(temp)

        for i in range(0,ck+2):
            self.ser.write(buff[i])
        self.doCheckSum(buff, ck)

    def readGPS(self):
        '''
        longitude and latitude are stored in a 4 byte struct [low_1, 2, 3, 4]
        '''
        buff = self.ser.read(14)
        longitude,latitude,altitude,gps_speed,blah = struct.unpack("<iihhh",buff)

        return [longitude,latitude,altitude,gps_speed]

    def sendRPY(self,longitude,latitude,altitude,ground_speed,ground_course,gps_time,imu_health):
        '''
        various GPS shit
        '''
        self.ser.write('DIYd')
        buff = [0x13,0x03]
        ck=19

        longitude = struct.pack('<l', longitude) # * 10^7 ? 4 bytes
        buff.extend(longitude)
        latitude = struct.pack('<l', longitude)  # * 10^7 ? 4 bytes
        buff.extend(latitude)

        altitude = struct.pack('<h', longitude) # meters, 2 bytes
        buff.extend(altitude)
        ground_speed = struct.pack('<h', longitude) # m/s * 100, 2 bytes
        buff.extend(ground_speed)
        ground_course = struct.pack('<l', longitude) # course in degrees * 100, 2 bytes
        buff.extend(ground_course)
        gps_time = struct.pack('<l', longitude) # ? 4 bytes
        buff.extend(gps_time)

        # write data to the serial port
        for i in range(0,ck+2):
            self.ser.write(buff[i])

        self.doCheckSum(buff, ck)

if __name__ == '__main__':
    imu = ArduIeMU(sys.argv[1],38400)
    p = Process(target=imu.loop(), args=())
    p.start()
    p.join()
