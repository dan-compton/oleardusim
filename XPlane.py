'''
Created on Oct 4, 2011

@author: dan compton (dniced -> lol@auburn.edu)

Represents an interface to XPlane.  Receives XPlane data associated with a particular ardupilot board.
Sends relevant data to associated board.  Also provides interface for ardupilot board to write controls
data to its associated XPlane simulator.
'''
import socket
from threading import Thread
from multiprocessing import Process
import serial
import struct 
import time
import sys

class XPlane(object):
    def __init__(self, xplane_recv_ip, xplane_recv_port,xplane_send_ip,xplane_send_port,GCS,ID):
        # UDP for xplanek
        self.xplane_recv_port = xplane_recv_port
        self.xplane_recv_ip = xplane_recv_ip
        self.xplane_send_port = xplane_send_port
        self.xplane_send_ip = xplane_send_ip
        self.ID = ID
        
        # reference to the ground control station
        # provides xplane<->ardupilot mappping
        self.GCS = GCS

        # Running?
        self.run = True

    def execute(self):
        xplaneRECV = Thread(target = self.xplaneThread, args=())
        xplaneRECV.start()

    def die(self):
        self.run = False

    def getID(self):
        return self.ID

    def processXPlaneUDP(self, data):
        vindKIAS,vindKEAS,vtrueKTAS,vtrueKTGS,f0,vindMPH,vtrueMPHAS,vtrueMPHGS = struct.unpack("<ffffffff", data[0:32])
        elev,ailrn,ruddr,f1,nwhel,f2,f3,f4= struct.unpack("<ffffffff", data[36:68])
        pitch,roll,hdingTRUE,hdingMAG,magCOMP,f5,f6,mavarDEG = struct.unpack("<ffffffff", data[72:104])
	latDEG,lonDEG,altFTMSL,altFTAGL,f7,altIND,latSOUTH,latWEST = struct.unpack("ffffffff",data[108:140])

        return {"roll":roll,"pitch":pitch,"lat":latDEG, "lon":lonDEG,"alt":altFTAGL,"airspeed":vtrueMPHAS,"speed":vtrueMPHGS,"heading":hdingTRUE}

    def writeControlsData(self, data):
        '''
        Sends controls data to xplane instance
        parms {throttle,roll,pitch,rudder}
        '''
        throttle = float(data["throttle"])
        roll = float(data["roll"])
        pitch = float(data["pitch"])
        rudder = float(data["rudder"])
        pream = "DATA0" 
        throttle_data = struct.pack("iffffffff",25,throttle,throttle,throttle,throttle,throttle,throttle,throttle,throttle)
        control_surface_data = struct.pack("ifffifiii",11,pitch,roll,0, -999,roll,-999,-999,-999)
        ardupilot_data = pream+throttle_data+control_surface_data
        self.sock.sendto(ardupilot_data,(self.xplane_send_ip,self.xplane_send_port))

    def xplaneThread(self):
        start = time.time()

        # Bind to socket to listen for incoming xplane data
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.xplane_recv_ip, self.xplane_recv_port))

        while self.run == True:
            xplane_data, addr = self.sock.recvfrom(256)
            if xplane_data[0] == 'D' and xplane_data[1] == 'A':
                # Get the xplane_data
                xplane_data = self.processXPlaneUDP(xplane_data[9:170])
                ardupilot = self.GCS.getArdupilot(self.ID)
                ardupilot.writeIMUData(xplane_data)
                
                # Send GPS data at about 5hz
                if time.time() - start > 0.20:
                    ardupilot.writeGPSData(xplane_data)
                    start = time.time() 
