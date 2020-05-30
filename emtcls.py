import numpy as np
import config
import elements as el
import dataloader as dl
import matplotlib.pyplot as plt
import scipy.linalg as la

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
        print("IH",self.I_H,"\n")
        print("Vn",self.Vn,"\n")
       

    def Gdivide(self):
        print("Modifying the conductance matrix...\n")        

        self.G_UU = self.G[0:self.unknownNodes,0:self.unknownNodes]
        print("G_UU",self.G_UU)
        print("\n")

        self.G_UK = self.G[0:self.unknownNodes,self.unknownNodes:self.numNodes]
        print("G_UK",self.G_UK)
        print("\n")

        self.G_KU = self.G[self.unknownNodes:self.numNodes,0:self.unknownNodes]
        print("G_KU",self.G_KU)
        print("\n")

        self.G_KK = self.G[self.unknownNodes:self.numNodes,self.unknownNodes:self.numNodes]
        print("G_KK",self.G_KK)
        print("\n")


    def LU(self):
        (P, L, U) = la.lu(self.G_UU)
        self.G_UU=U
        print("G_UU after LU decom",self.G_UU)
        print("\n")

    def IVdevide(self):
        self.V_K=self.Vn[0:self.src_cont] 
        print("V_K",self.V_K)
        print("\n")

        self.V_U=self.Vn[0:self.unknownNodes]
        print("V_U",self.V_U)
        print("\n")

        self.I_K=self.I_H[0:self.src_cont]
        print("I_K",self.I_K)
        print("\n")

        
        self.I_U = self.I_H[0:self.unknownNodes]
        print("I_U",self.I_U)

        print("\n ///////////////////////////////////////// \n")






    def calcBrnHistory(self,TheTime):
        for obj in self.comp_list:
            if obj.brnType=="R":
               obj.ihistory=0.0
            elif obj.brnType=="S":
                obj.Sourceupdate(TheTime)
                #print("source hisory",obj.ihistory)
            elif obj.brnType=="L":
                obj.ihistory=obj.Ilast+obj.Vlast/obj.Reff
            elif obj.brnType=="C":
                obj.ihistory=-obj.Ilast-obj.Vlast/obj.Reff
            else:
                print("Only R L C S elements considered")
            
            print("history of branch",obj.ihistory,"\n")

    def calcinjection(self):

        self.I_H=np.zeros((self.numNodes, 1))

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

        print("I_H",self.I_H)

    def calcnewV(self):
        self.V_U=np.linalg.solve(self.G_UU, self.I_U ) 
        print("Vn",self.V_U)


    def reconstruct_V(self):
        self.Vn=np.concatenate([self.V_U,self.V_K])
        print("Vn",self.Vn)

    def reconstruct_I(self):
        print("IU",self.I_U)
        print("IK",self.I_K)
        self.I_K=np.matmul(self.G_KU,self.V_U)+ np.matmul(self.G_KK,self.V_K)-self.I_H[self.unknownNodes:self.numNodes] 
        self.I_U = self.I_U - np.matmul(self.G_UK,self.V_K)
        self.I_H=np.concatenate([self.I_U,self.I_K])
        print("I_H",self.I_H)
        print("delthis",self.I_H[self.unknownNodes:self.numNodes] )



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
                obj.I_last = V/obj.Reff+obj.ihistory
            elif obj.brnType == "L":
                obj.I_last = V/obj.Reff + obj.ihistory
            elif obj.brnType == "C":
                obj.I_last = V/obj.Reff + obj.ihistory



            

        

        
            
            
