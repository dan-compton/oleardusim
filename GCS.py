'''
Created on Oct 23, 2011

@author: dan compton (dniced -> lol@auburn.edu)

Full python ground control station which can control multiple UAVs, collision avoidance, and display
results in google maps and XPlane
'''
import socket
from threading import Thread
from multiprocessing import Process
import random
from random import sample
import serial
import struct 
import time
import sys
import XPlane
import ArduPilot
import pylab
import matplotlib
import matplotlib.pyplot as plt
from pyproj import Proj

class GCS(object):
    def __init__(self):
        # We don't want the objects to be aware of their linkages
        self.ID_to_ardu = {}
        self.ID_to_xplane = {}
        self.xplane_to_ardu_map = {}
        self.ardu_to_xplane_map = {}
        
        self.gps_update_constraint = 3
        self.gps_timer = time.time()
    
    def add_pair(self,ardupilot,xplane):
        self.ID_to_ardu[ardupilot.getID()] = ardupilot
        self.ID_to_xplane[xplane.getID()] = xplane
        self.xplane_to_ardu_map[xplane.getID()] = ardupilot
        self.ardu_to_xplane_map[ardupilot.getID()] = xplane

    def get_xplane(self,ardupilot_id):
        return self.ardu_to_xplane_map[ardupilot_id]

    def get_ardupilot(self,xplane_id):
        return self.xplane_to_ardu_map[xplane_id]

    def get_current_plane_positions(self,notPlane=None):
        '''
        returns a list of all current locations of planes
        (except notPlane's)
        '''
        plane_positions = []
        for key in self.ardu_to_xplane_map:
            plane = self.ID_to_ardu[key]
            if plane.getID() != notPlane.getID():
                plane_positions.append((plane.getLastLoc()[0],plane.getLastLoc()[1]))
        return plane_positions
  
    def die(self):
        # kill off all processes
        for key in self.ID_to_xplane:
            self.ID_to_xplane[key].die()
        for key in self.ID_to_ardu:
            self.ID_to_ardu[key].die()

