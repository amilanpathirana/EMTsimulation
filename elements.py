import numpy as np
import config

class Branch():
    def __init__(self,brnType,strnode,stpnode,Ilast,Vlast,value):
        self.brnType=brnType
        self.strnode=strnode
        self.stpnode=stpnode
        self.Ilast=Ilast
        self.Vlast=Vlast
        self.Isource=0

        

        if self.brnType=="R":
            self.Reff=value
        elif self.brnType=="S":
            self.Reff=value
        elif self.brnType=="L":
            self.Reff=2*value/config.Dt
        elif self.brnType=="C":
            self.Reff=config.Dt/2*value
        else:
            print("Only R L C S elements considered")

class Source():
    def __init__(self,brnType,strnode,stpnode,magnitude,angle,frequency,value):
        self.brnType = brnType
        self.strnode= strnode
        self.stpnode= stpnode
        self.magnitude= magnitude
        self.angle= angle
        self.frequency= frequency
        self.Reff=value
        self.Isource=0
        self.Vlast=0.0
        self.ihistory=0.0
    def Sourceupdate(self,TheTime):
        I_mag = self.magnitude
        I_ang = self.angle
        freq = self.frequency
        self.ihistory = I_mag*np.sin(2.0*np.pi*self.frequency*TheTime + I_ang*np.pi/180.0)
        




