import numpy as np
import config
import elements as el
import dataloader as dl
import matplotlib.pyplot as plt

class EMT:
    def __init__(self):
        self.comp_list = dl.elemet_list

        src_count=0
        for obj in self.comp_list:
            #print(obj.brnType)
            if obj.brnType=="S":
                src_count=src_count+1
        self.src_cont=src_count

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
        self.unknownNodes=self.numNodes-self.src_cont

        self.numBranches=len(self.comp_list)
        
        self.vol=[]
        for i in range(self.numNodes):
            self.vol.append(0)

        self.I_History=[]
        for i in range(self.numNodes):
            self.I_History.append(0)
        self.trace=[]

    def formG(self):
        #print("\nGenerating the conductance matrix...")
        self.G = np.zeros((self.numNodes,self.numNodes))
        for obj in self.comp_list:
            From = obj.strnode
            To = obj.stpnode
            
            if To==0 and From==0:
                print("*** Both nodes of a element is zero ***")
            
            if To==From:
                print("*** Both nodes of a element is same ***")

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
            
        #print("Conductance matrix:\n ",self.G)


    def Gremake(self):
        print("No of sources",self.src_cont)
        self.unknownNodes=self.numNodes-self.src_cont
        print("No of unknown nodes",self.unknownNodes)

        
        G_UU = self.G[0:self.unknownNodes,0:self.unknownNodes]
        print("GUU",G_UU)
        print(self.G)

        G_UK = self.G[0:self.unknownNodes-1,self.unknownNodes:self.numNodes]
        print("GUK",G_UK)

        print(self.I_History)
        I_U = self.I_History[0:self.unknownNodes]
        print("IU",I_U)

        V_K=self.vol[0:self.src_cont] 
 
        print("VK",V_K)
        I_d_history=self.I_History[0:self.unknownNodes]
        I_d_history = I_U - G_UK*V_K

        print("idhis",I_d_history)

        invG=np.linalg.inv(G_UU)
        #V_U=np.matmul(invG,I_d_history)
        

        

        #print("VU",V_U)

        #V_n(1:No_UnkownNodes,1) = V_U
        
        #V_n(No_UnkownNodes+1:No_Nodes,1)=V_K


    def calcBrnHistory(self,TheTime):
        for obj in self.comp_list:
            if obj.brnType=="R":
               obj.ihistory=0
            elif obj.brnType=="S":
                obj.Sourceupdate(TheTime)
            elif obj.brnType=="L":
                obj.ihistory=obj.Ilast+obj.Vlast/obj.Reff
            elif obj.brnType=="C":
                obj.ihistory=-obj.Ilast-obj.Vlast/obj.Reff
            else:
                print("Only R L C S elements considered")
            
            #print(obj.ihistory)

    def calcinjection(self):
        for i in range(len(self.I_History)):
            self.I_History[i]=0.0

        for obj in self.comp_list:
            Type = obj.brnType
            From = obj.strnode-1
            To = obj.stpnode-1

            Brn_I_History = obj.ihistory
            #print(Brn_I_History)
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
                    pass

        #print(self.I_History)

    def calcnewV(self):


        invG=np.linalg.inv(self.G)
        self.vol=np.matmul(invG,self.I_History)
        print("vol",self.vol)


    def recordv(self,node):
        self.trace.append(self.vol[node-1])

    def plotv(self):
        plt.close('all')
        plt.plot(self.trace)
        plt.show()







    def calcNewbranchI(self):
        for obj in self.comp_list:
            Type = obj.brnType
            From = obj.strnode-1
            To = obj.stpnode-1
            if From==-1:
                V = self.vol[To]
            if To==-1:
                V = -self.vol[To]
            else:
                V=self.vol[From]-self.vol[To]
            obj.Vlast=V
            #print("To",To)
            if obj.brnType == "R":
                obj.I_last = V/obj.Reff
            elif obj.brnType == "S":
                obj.I_last = V/obj.Reff
            elif obj.brnType == "L":
                obj.I_last = V/obj.Reff + obj.ihistory
            elif obj.brnType == "C":
                obj.I_last = V/obj.Reff + obj.ihistory



            

        

        
            
            
