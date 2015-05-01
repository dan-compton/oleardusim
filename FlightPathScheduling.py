'''
Created on Oct 23, 2011

@author: dan compton (dniced -> lol@auburn.edu)

'''
import time
import sys
import XPlane
import ArduPilot
from pyproj import Proj
import matplotlib.pyplot as plt
import networkx as nx
import random
import math
from random import sample

       
class AStar(object):
    
    def heuristic_cost_estimate(self,node,goal):
        '''
        Simply returns straight line distance
        '''
        return math.sqrt(math.pow(goal[0]-node[1],2)+math.pow(node[0]-node[1],2))

    def reconstruct_path(self,came_from,path,current_node): 
        while came_from[current_node] in came_from:
            path.append(current_node)
            current_node = came_from[current_node]
        return path

    def execute(self,graph,static_object_field_utm,start_utm,goal_utm):
        start = (graph.coord_map_x[start_utm[0]],graph.coord_map_y[start_utm[1]],)
        goal = graph.interpolateGoalNode(goal_utm)  
        
        static_obj_nodewise = []
        closedset = []
        openset = [start]
        came_from = {}
        g_score = {}
        h_score = {}
        f_score = {}

        g_score[start] = 0      # cost along best known path
        h_score[start] = self.heuristic_cost_estimate(start,goal) 
        f_score[start] = g_score[start]+h_score[start]

        # Prevent traversal to obstacles
        for i in static_object_field_utm:
            if i[0] in graph.coord_map_x and i[1] in graph.coord_map_y:
                sx,sy = graph.coord_map_x[i[0]],graph.coord_map_y[i[1]] 
                closedset.append((sx,sy,))
                static_obj_nodewise.append((sx,sy,))

        while len(openset) > 0:
            # Set x to minimum of f_score
            x = None
            for key in openset:
                if x == None or f_score[key] < f_score[x]:
                    x = key
            if x==goal:
                return self.reconstruct_path(came_from,[],came_from[goal])
            
            openset.remove(x)
            closedset.append(x)
            for i in graph.G.neighbors(x):  
                if i in closedset:
                    continue
                tentative_g_score = g_score[x] + 1 

                if i not in openset:
                    openset.append(i)
                    tentative_is_better = True
                elif tentative_g_score < g_score[i]:
                    tentative_is_better = True
                else:
                    tentative_is_better = False
                
                if tentative_is_better == True:
                    came_from[i] = x
                    g_score[i] = tentative_g_score
                    h_score[i] = self.heuristic_cost_estimate(i,goal)
                    f_score[i] = g_score[i] + h_score[i]

        print 'NO SOLUTION!'
        graph.drawGraph(start_utm,static_object_field_utm,[goal_utm],[])
        return []
