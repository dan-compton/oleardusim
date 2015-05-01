import networkx as nx
import math
import sys
import random
from random import sample

class DiscretizedUTMGrid(object):
    def __init__(self,current_loc, width, height,res):
        self.dx = res[0]
        self.dy = res[1]
        self.px = current_loc[0]
        self.py = current_loc[1]
        self.height = height
        self.width = width
        self.coord_map = {}
        self.coord_map_x = {}
        self.coord_map_y = {}
        self.node_map = {}

        # Create nx representation of graph
        self.G = nx.grid_2d_graph(width/self.dx,height/self.dy)
        for n in self.G:
            x,y = n
            if (x-1,y+1,) in self.G.nodes():
                self.G.add_edge(n,(x-1,y+1))
            if (x+1,y+1,) in self.G.nodes():
                self.G.add_edge(n,(x+1,y+1))

        # map coordinates to graph nodes
        row,col = 0,0
        rc,cc = 0,0
        for i in range(self.px, self.px+width):
            cc += 1
            if cc >= self.dx:
                cc = 0
                col += 1
            self.coord_map_x[i] = col
            row = 0
            for j in range(self.py,self.py+height):
                rc += 1
                if rc >= self.dy:
                    rc = 0
                    row += 1
                self.coord_map_y[j] = row
                utm_node = (i,j,)
                node = (col,row,)
                self.coord_map[utm_node] = node
                if node in self.node_map:
                    self.node_map[node].extend([utm_node])
                else:
                    self.node_map[node] = [utm_node]

    def getNodeUTM(self,node):
        utm_x = 0
        utm_y = 0
        for i in self.node_map[node]:
            utm_x += i[0]
            utm_y += i[1]
        utm_x = utm_x/len(self.node_map)
        utm_y = utm_y/len(self.node_map)
        return (utm_x,utm_y,)

    def interpolateGoalNode(self,goal):
        '''
        If the goal node lies outside of the grid,
        returns the node closes to the goal by straight line
        distance
        '''
        distance = None
        goal_interp = None
        if len(self.coord_map) == 0:
            print "FUCK"
        for i in self.coord_map:
            temp_dist = math.pow(goal[0] - i[0],2)+math.pow(goal[1]-i[1],2)
            if distance == None:
                distance = temp_dist
            if temp_dist <= distance:
                goal_interp = self.coord_map[i]
        return goal_interp

    def drawGraph(self,current_loc,static_object_field,goals,path):
        pos = {}
        for i in self.G.nodes():
            pos[i] = i

        # Remove the plane node
        planeNode = (self.coord_map_x[current_loc[0]],self.coord_map_y[current_loc[1]])
        nodeList = self.G.nodes()
        nodeList.remove(planeNode)

        # Remove the Goal node
        goalList = []
        for i in goals:
            j = (self.coord_map_x[i[0]],self.coord_map_y[i[1]],)
            if j in nodeList:
                nodeList.remove(j)
                goalList.append(j)

        # Remove the pathlist from the object field
        pathList = []
        for i in path:
            sx,sy = i[0],i[1]
            if ((sx,sy,) in nodeList):
                nodeList.remove((sx,sy,))
                pathList.append((sx,sy,))

        # Remove all objects in the object field
        objectField = []
        for i in static_object_field:
            if i[0] in self.coord_map_x and i[1] in self.coord_map_y:
                sx,sy = self.coord_map_x[i[0]],self.coord_map_y[i[1]]
                if ((sx,sy,) in nodeList):
                    nodeList.remove((sx,sy,))
                    objectField.append((sx,sy,))

        nx.draw_networkx_nodes(self.G,pos,node_color='r',node_size=50,nodelist=[planeNode])
        nx.draw_networkx_nodes(self.G,pos,node_color='y',node_size=50,nodelist=goalList)
        nx.draw_networkx_nodes(self.G,pos,node_color='r',node_size=50,nodelist=pathList)
        nx.draw_networkx_nodes(self.G,pos,node_color='g',node_size=50,nodelist=objectField)
        nx.draw_networkx_nodes(self.G,pos,node_color='b',node_size=50,nodelist=nodeList)
        nx.draw_networkx_edges(self.G,pos,alpha=0.5,width=1)
        plt.show()

    def generateStaticObjectField(self,current_loc, width, height, num):
        center_x,center_y = current_loc[0], current_loc[1]
        x = []
        y = []
        points = []
        for i in range(int(center_x)-width/2,int(center_x)+width/2):
            for j in range(int(center_y),int(center_y + height)):
                points.append((i,j,))
                x.append(i)
                y.append(j)
        points = random.sample(points,num)
        return points
