import numpy as np
import config
class RLC():
    def __init__(self,brnType,strnode,stpnode,Ilast,Vlast,value):
        self.brnType=brnType
        self.strnode=strnode
        self.stpnode=stpnode
        self.Ilast=Ilast
        self.Vlast=Vlast           

        if self.brnType=="R":
            self.Reff=value
        elif self.brnType=="L":
            self.Reff=2*value/config.Dt
        elif self.brnType=="C":
            self.Reff=config.Dt/2*value
        else:
            print("Only R L C elements considered")

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
        self.ihistory = self.magnitude*np.cos(2.0*np.pi*self.frequency*TheTime + self.angle*np.pi/180.0)
        


class Switch():
    stoptogle=0
    def __init__(self,brnType,strnode,stpnode,Ilast,Vlast,valueon,valueoff,togletime,status=1):
        self.brnType=brnType
        self.strnode=strnode
        self.stpnode=stpnode
        self.Ilast=Ilast
        self.Vlast=Vlast
        self.valueon=valueon
        self.valueoff=valueoff
        self.status=status
        self.ihistory=0.0
        

        if self.status==1:
            self.Reff=self.valueon
        elif self.status==0:
            self.Reff=self.valueoff

    def togle(self):
        print(self.status)
        if stoptogle==0:
            if self.status==1:
                self.status=0
                stoptogle=1

            elif self.status==0:
                self.status=1
                stoptogle=1

        print("Togled",self.status)
        if self.status==1:
            self.Reff=self.valueon
        elif self.status==0:
            self.Reff=self.valueoff

                    


        