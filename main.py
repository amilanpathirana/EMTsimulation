import numpy as np
import config
import elements as el
import dataloader as dl

class EMT:
    def __init__(self):
        self.comp_list = dl.elemet_list
        
        for obj in self.comp_list:
            if obj.brnType=="S":
                self.S1=obj


        #max node number
        maxnode=0
        for obj in self.comp_list:
            From = obj.strnode
            To = obj.stpnode
            if From > maxnode:
                maxnode=From
            if To > maxnode:
                maxnode=To
        self.numNodes=maxnode
        self.numBranches=len(self.comp_list)
        
        self.vol=[]
        for i in range(self.numNodes):
            self.vol.append(0)

        self.I_History=[]
        for i in range(self.numNodes):
            self.I_History.append(0)

        self.I_History_src=[]
        for i in range(self.numNodes):
            self.I_History_src.append(0)

    def formG(self):
        self.G = np.zeros((self.numNodes,self.numNodes))
        for obj in self.comp_list:
            Type = obj.brnType
            From = obj.strnode
            To = obj.stpnode

            if To==0 and From==0:
                print("*** Both Nodes Zero ***")
            
            if To==From:
                print("*** Both Nodes Same ***")

            Series = 1
            if To == 0:
                To = From
                Series = 0
                
            if From == 0:
                From = To
                Series = 0
              

             
            obj.Series=Series

            To=To-1
            From=From-1
            if obj.Series==1:
                self.G[To,To] = self.G[To,To] + 1/obj.Reff
                self.G[From,From] = self.G[From,From] + 1/obj.Reff
                self.G[From,To] = self.G[From,To] - 1/obj.Reff
                self.G[To,From] = self.G[To,From] - 1/obj.Reff
            else:
                self.G[To,To] = self.G[To,To] + 1/obj.Reff
            
        print(self.G)
 
    def calcBrnHistory(self):
        for obj in self.comp_list:
            if obj.brnType=="R":
               obj.ihistory=0
            elif obj.brnType=="S":
                obj.ihistory= 0
            elif obj.brnType=="L":
                obj.ihistory=obj.Ilast+obj.Vlast/obj.Reff
            elif obj.brnType=="C":
                obj.ihistory=-obj.Ilast-obj.Vlast/obj.Reff
            else:
                print("Only R L C S elements considered")
            
            #print(obj.ihistory)

    def calcinjection(self):
        for obj in self.comp_list:
            Type = obj.brnType
            From = obj.strnode-1
            To = obj.stpnode-1

            Brn_I_History = obj.ihistory
            if obj.Series==1:
            #Series Component
                self.I_History[To] = self.I_History[To] + Brn_I_History
                self.I_History[From] = self.I_History[From]- Brn_I_History
            else:
                if To== 0:
                    self.I_History[To] = self.I_History[To] + Brn_I_History
                elif From== 0:
                    self.I_History[From] = self.I_History[From]- Brn_I_History
                else:
                    print("*** ***")

        print(self.I_History)

    def calcnewV(self):
        invG=np.linalg.inv(self.G)
        self.vol=np.matmul(invG,self.I_History)
        print("vol",self.vol)

    def updateVol(self,TheTime):
        for obj in self.comp_list:
            Type = obj.brnType
            From = obj.strnode-1
            To = obj.stpnode-1
            self.TheTime=TheTime
            self.I_History_src[2] = self.S1.Sourceupdate(self.TheTime)
       
        self.I_History=np.add(self.I_History,self.I_History_src)

    def calcNewbranchI(self):
        for obj in self.comp_list:
            Type = obj.brnType
            From = obj.strnode-1
            To = obj.stpnode-1

            V = obj.Vlast

            if obj.brnType == "R":
                obj.I_last = V/obj.Reff
            elif obj.brnType == "S":
                obj.I_last = V/obj.Reff
            elif obj.brnType == "L":
                obj.I_last = V/obj.Reff + obj.ihistory
            elif obj.brnType == "C":
                obj.I_last = V/obj.Reff + obj.ihistory

        

        
            
            



def run():
    print("run")
    Time=config.srtTime
    EMTDC=EMT()

    EMTDC.formG()

    while Time<config.stpTime:
        
        print(Time,config.stpTime)
        Time=Time+config.Dt

        EMTDC.updateVol(Time)

        EMTDC.calcBrnHistory()

        EMTDC.calcinjection()

        EMTDC.calcnewV()

        EMTDC.calcNewbranchI()


run()