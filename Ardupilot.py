'''
Created on Oct 23, 2011

@author: dan compton (dniced -> lol@auburn.edu)

Represents an instance of an ArduPilot board.
'''
import socket
from threading import Thread
import serial
import struct 
import time
import sys

class ArduPilot(object):
    def __init__(self,ardu_id,ardu_comport, ardu_baud):
        # serial interface for communicating with the ardupilot board
        self.ardu_comport = ardu_comport
        self.ardu_baud = ardu_baud
        self.ardu_id = ardu_id
        
        #TODO add communication mediator/strategy to provide uniform interface
        # for serial communication (e.g. Xbee OR FTDI).
        # This will require additional modification to ArduPilot backend code
        self.ser = serial.Serial(self.ardu_comport, self.ardu_baud)

        # Start a loop to receive data from the ardupilot
        ardupilotRECV = Thread(target = self.ardupilotThread, args=()) 
        ardupilotRECV.start()
        ardupilotRECV.join()

        self.run = True

    def die(self):
        self.run = False

    def constrain(self, data, minv,maxv):
        if data > maxv:
            data = maxv
        elif data < minv:
            data = minv
        return data

    def processArduPilot(self, data):
        '''
        Process controls data that we read from the ardupilot to send
        to things like FlightGear or XPlane
        '''
        roll,pitch,throttle = struct.unpack("<hhh", data[0:6])
        rudder,wp_distance,bearing_error = struct.unpack("<hhh", data[6:12])
        alt_error,eng_error,wp_index,control_mode = struct.unpack("<hhbb", data[12:18])

        # apply gains/convert to floats
        roll = self.constrain(float(roll)/6000.0,-1,1)
        pitch = self.constrain(float(pitch)/6000.0,-1,1)
        throttle = self.constrain(float(throttle)/100.0,-1,1)

        return {"roll":roll,"pitch":pitch,"throttle":throttle,"rudder":rudder} 

    def calculateChecksum(self, buff):
        '''
        Calculates the checksum required for Ardupilot Payload data and packs it into a string.
        '''
        check_a, check_b = 0,0
        for i in buff:
            check_a = check_a + i
            check_b = check_b + check_a
        checksum = struct.pack("BB",(check_a&0xff),(check_b&0xff))

        return checksum

    def writeToArdupilot(self,message_body):
        '''
        Writes to the ardupilot (currently) via the FTDI serial interface
        '''
        pream = 'DIYd'
        bytewise_body = struct.unpack('b'*len(message_body), message_body)
        ck_a,ck_b = self.calculateChecksum(self,bytewise_body)
        full_message = pream+full_body+ck_a+ck_b
        self.ser.write(full_message)

    def writeGPSDestination(self,data):
        '''
        Sets a new GPS waypoint on the given ArduPilot.  The autopilot will immediately course correct
        and travel to the new location. This essentially changes the current HOME location and utilizes
        RTL to travel to that point.
        params {lat,lon,alt}
        '''
        lat = int(data["lat"] * 10000000)
        lon = int(data["lon"] * 10000000)
        alt = int(data["alt"] * 3.48)
        message_body = struct.pack("=bbiiHHH",14,5,lon,lat,alt,1,1)
        self.writeToArdupilot(message_body)

    def writeIMUData(self,data):
        '''
        Writes IMU data from a simulator to the ArduPilot. 
        params {roll,pitch,heading,airspeed}
        '''
        roll = int(data["roll"]*100)
        pitch = int(data["pitch"]*100)
        heading = int(data["heading"]*100)
        airspeed = int(data["airspeed"]*44.704)
            
        message_body = struct.pack("bbhhHH",8,4,roll,pitch,heading,airspeed)
        self.writeToArdupilot(message_body)

    def ardupilotThread(self):
        while self.run == True:
            try:
                buff = self.ser.readline()
                if buff[0] == 'M':
                    print buff
                if buff[0] == 'A' and buff[1] == 'A' and buff[2] == 'A':
                    if sys.getsizeof(buff) == 60:
                        ardupilot_data = self.processArduPilot(buff[3:-1])
                        self.writeArduPilotData(ardupilot_data)
            except KeyboardInterrupt:
                break
