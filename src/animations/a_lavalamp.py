import pyghthouse.utils as utils
from random import random
import math

class Lavalamp():
    
    class Node():
        def __init__(self, col, nodeVel):
            self.x = 30*random()-1
            self.y = 30*random()-1
            self.col = random()
            self.acc = random()-0.5

        def update(self):
            self.changeColor()

        def changeColor(self):
            self.acc = self.acc + pow(random(), 2) * 0.3
            sinAcc = math.sin(self.acc) * 0.05
            dist = 0
            if sinAcc > 0:
                dist = 1 - self.col
            else:
                dist = self.col
            self.col = self.col + sinAcc * dist

    class MovingNode(Node):
        def __init__(self, col, nodeVel):
            super().__init__(col, nodeVel)
            self.col= col
            self.xVel = nodeVel * (random() - 0.5)
            self.yVel = nodeVel * (random() - 0.5)

        def update(self):
            self.move()
            #self.changeColor()

        def move(self):
            self.x += self.xVel
            self.y += self.yVel
            if self.y > 29:
                self.yVel *= -1
                self.y = 29
            
            if self.x > 29:
                self.xVel *= -1
                self.x = 29

            if self.y < 0:
                self.yVel *= -1
                self.y = 0

            if self.x < 0:
                self.xVel *= -1
                self.x = 0

    class LavaNode(MovingNode):
        def __init__(self, col, nodeVel):
            super().__init__(col, nodeVel)
            self.col = col
            self.nodeVel = nodeVel
            self.y = 35

        def update(self):
            self.move()

        def move(self):
            self.xVelByHeight()
            self.xMove()
            self.xBounce(0.2)
            self.yMove()

        def xVelByHeight(self):
            xRel = (self.x +1) / 30
            yRel = (self.y +1) / 30 - 0.5
            if (abs(yRel) < 0.5):
                if (xRel < 0.5):
                    self.xVel += (yRel * 0.002 * self.nodeVel)
                else:
                    self.xVel -= (yRel * 0.002 * self.nodeVel)

        def xMove(self):
            pass

        def yMove(self):
            self.y -= math.cos(math.pi *(((self.x +1) / 15) -1)) * self.nodeVel

        def xBounce(self, factor):
            self.x += self. xVel
            if self.x > 29:
                self.xVel *= -factor
                self.x = 29

            if self.x < 0:
                self.xVel *= -factor
                self.x = 0

    def setup(self):
        self.nodes = []
        for i in range(0, self.numNodes):
            self.nodes.append(self.LavaNode(i, self.nodeVel))
    
    def draw(self):
        self.step()
        if random() < self.spawnChance:
            self.nodes.append(self.LavaNode(1, self.nodeVel))
        self.hue += 0.0001
        if self.hue > 1.0:
            self.hue = 0
        for x in range(0,28):
            for y in range(0,14):
                c = self.calcCol(x, 2*y)
                # TODO: Original is hsl. Add hsl color calculation
                self.frame[x][y] = utils.from_hsv(0.55, 0.8, c)
                #self.frame[x][y] = [255*c,127*c,0] # orange

    def map(self, val, istart, istop, ostart, ostop):
        return ostart + (ostop - ostart) * ((val - istart) / (istop - istart))
    
    def colNearestNeighbour(self, x, y):
        nearestNode = self.nodes[0]
        nearestNodeDist = pow((nearestNode.x -x), 2) + pow ((nearestNode.y - y), 2)
        for i in range(len(self.nodes)):
            dist = pow(self.nodes[i].x - x, 2) + pow(self.nodes[i].y - y, 2)
            if dist < nearestNodeDist:
                nearestNodeDist = dist
                nearestNode = self.nodes[i]
        return nearestNode.col
    
    def colSinglePixelDebug(self,x,y):
        nearestNode = self.nodes[0]
        nearestNodeDist = pow((nearestNode.x - x), 2) + pow ((nearestNode.y - y), 2)
        for i in range(len(self.nodes)):
            dist = pow(self.nodes[i].x - x, 2) + pow(self.nodes[i].y - y, 2)
            if dist < nearestNodeDist:
                nearestNodeDist = dist
                nearestNode = self.nodes[i]
        if nearestNode < 1:
            return 0
        return nearestNode.col
    
    def colSinglePixelBloom(self, x, y):
        nearestNode = self.nodes[0]
        nearestNodeDist = pow((nearestNode.x - x), 2) + pow ((nearestNode.y - y), 2)
        for i in range(len(self.nodes)):
            dist = pow(self.nodes[i].x - x, 2) + pow(self.nodes[i].y - y, 2)
            if dist < nearestNodeDist:
                nearestNodeDist = dist
                nearestNode = self.nodes[i]
        return (min(self.colWeightedAverage(x,y) / math.sqrt(nearestNodeDist) * self.colSPBloomStrength, 1))
    
    def colWeightedAverage(self,x,y):
        dists = []
        val = 0
        vals = []
        for i in range(len(self.nodes)):
            dists.append(math.sqrt(pow(self.nodes[i].x-x, 2) + pow(self.nodes[i].y-y, 2)))
            vals.append(math.exp(-dists[i]))
            val += vals[i]
        res = 0
        for i in range(len(self.nodes)):
            res += vals[i] * self.nodes[i].col
        return res/val
    
    def calcCol(self, x,y):
        return self.colorCalculation(x,y)
    
    def step(self):
        for i in range(len(self.nodes)):
            self.nodes[i].update()

    def sigma(self, x):
        return 1 / (1 + math.exp(-x))
    

    def c_dist(self, x, y):
        closest_dist = math.inf
        for node in self.nodes:
            dist = math.pow(node.x - x, 2) + math.pow(node.y - y, 2)
            if dist < closest_dist:
                closest_dist = dist

        c = (1 / (math.sqrt(closest_dist) + 0.00001)) * self.colSPBloomStrength
        if c > 1:
            c = 1
        return c

    @staticmethod
    def get_instance(xsize, ysize, fps=60):
        instance = Lavalamp()
        instance.params()
        return instance

    def params(self):
        self.xsize = 28
        self.ysize = 14
        self.fps = 60
        self.name = "Lavalamp"

        self.nodeVel = 0.1
        self.numNodes = 50
        self.spawnChance = 0
        #self.colorCalculation = self.colSinglePixelBloom
        self.colorCalculation = self.c_dist
        self.startCol = lambda i : 1
        self.colSPBloomStrength = 1.5
        self.hue = 0
        self.nodes = []
        self.setup()


    def get_frame(self):
        self.set_frame()
        return self.frame
    
    def set_frame(self):
        self.draw()


    def __init__(self, xsize=28, ysize=14, fps=60):
        self.name = "Lavalamp"
        self.xsize = 28
        self.ysize = 14
        self.fps = 60
        
        self.frame=[]
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.nodeVel = 0.1
        self.numNodes = 50
        self.spawnChance = 0
        #self.colorCalculation = self.colSinglePixelBloom
        self.colorCalculation = self.c_dist
        self.startCol = lambda i : 1
        self.colSPBloomStrength = 2 #1.5
        self.hue = 0
        self.nodes = []
        self.setup()