import numpy as np
import config
import elements as el
import dataloader as dl
import matplotlib.pyplot as plt

class Network:
    def __init__(self):

        self.comp_list = dl.elemet_list

        src_count=0
        for obj in self.comp_list:
            #print(obj.brnType)
            if obj.brnType=="S":
                src_count=src_count+1
        self.src_cont=src_count

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

        self.G = np.zeros((self.numNodes,self.numNodes))
        
        self.Vn=np.zeros((self.numNodes, 1))
        self.I_H=np.zeros((self.numNodes, 1))

        self.trace=[]

        print("No of sources",self.src_cont,"\n")
        print("No of unknown nodes",self.unknownNodes,"\n")


    def formG(self):
        print("Generating the conductance matrix...")
        
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
            
        print("Conductance matrix:\n ",self.G,"\n")
       

    def Gremake(self):
                  

        
        G_UU = self.G[0:self.unknownNodes,0:self.unknownNodes]
        print("GUU",G_UU)
        print("\n")
        

        G_UK = self.G[0:self.unknownNodes,self.unknownNodes:self.numNodes]
        print("GUK",G_UK)
        print("\n")

        I_U = self.I_H[0:self.unknownNodes]
        print("IU",I_U)
        print("\n")

        V_K=self.Vn[0:self.src_cont] 
        print("VK",V_K)
        print("\n")

        I_d_history=self.I_H[0:self.unknownNodes]
        I_d_history = I_U - G_UK*V_K
        print("idhis",I_d_history)
        print("\n ///////////////////////////////////////// \n")

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
        for i in range(len(self.I_H)):
            self.I_H[i]=0.0

        for obj in self.comp_list:
            Type = obj.brnType
            From = obj.strnode-1
            To = obj.stpnode-1

            Brn_I_H = obj.ihistory
            #print(Brn_I_H)
            if obj.Series==1:
            #Series Componentrt
                self.I_H[To] = self.I_H[To] + Brn_I_H
                self.I_H[From] = self.I_H[From]- Brn_I_H
            else:
                if To== 0:
                    self.I_H[To] = self.I_H[To] + Brn_I_H
                elif From== 0:
                    self.I_H[From] = self.I_H[From]- Brn_I_H
                else:
                    pass

        #print(self.I_H)

    def calcnewV(self):


        invG=np.linalg.inv(self.G)
        self.Vn=np.matmul(invG,self.I_H)
        print("Vn",self.Vn)


    def recordv(self,node):
        self.trace.append(self.Vn[node-1])

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
                V = self.Vn[To]
            if To==-1:
                V = -self.Vn[To]
            else:
                V=self.Vn[From]-self.Vn[To]
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



            

        

        
            
            
