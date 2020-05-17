import numpy as np
import config
class EMT:
    def __init__(self,numNodes):
        self.numNodes=numNodes
        self.G = np.zeros((self.numNodes,self.numNodes))
        self.list = [] 
        self.I_History=[]
        
        for i in range(self.numNodes):
            self.I_History.append(0)

    # Initialize [G] matrix to zero
    def formG(self):
        for i in range(self.numNodes):
            # appending instances to list  
            self.list.append(Branch("L",1,0,0,0,500e-6)) 
            self.list.append(Branch("R",2,1,0,0,100)) 
            self.list.append(Branch("S",3,2,0,0,10)) 
            self.list.append(Branch("C",3,0,0,0,100e-6))

        for obj in self.list:
            Type = obj.brnType
            From = obj.strnode
            To = obj.stpnode

            obj.Series = 1
            if To == 0:
                To = From
                obj.Series = 0
                
            if From == 0:
                From = To
                obj.Series = 0
                
            if To==0:
                print("*** Both Nodes Zero ***")


            if obj.Series==1:
                self.G[To,To] = self.G[To,To] + 1/obj.Reff
                self.G[From,From] = self.G[From,From] + 1/obj.Reff
                self.G[From,To] = self.G[From,To] - 1/obj.Reff
                self.G[To,From] = self.G[To,From] - 1/obj.Reff
            else:
                self.G[To,To] = self.G[To,To] + 1/obj.Reff
        
        return self.G, len(self.list)

    def calcBrnHistory(self):
        for obj in self.list:
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
        for obj in self.list:
            Type = obj.brnType
            From = obj.strnode
            To = obj.stpnode

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
                    print("*** Error: Both Nodes Zero ***")

            
            




class Branch():
    def __init__(self,brnType,strnode,stpnode,Ilast,Vlast,value):
        self.brnType=brnType
        self.strnode=strnode
        self.stpnode=stpnode
        self.Ilast=Ilast
        self.Vlast=Vlast
        self.Series=0

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


 



#Initialize G with 4X4
G=EMT(4)

# Add componets and form G matrix
g=G.formG()

G.calcBrnHistory()
G.calcinjection()
print(g)

# Update sources

# Calculate history









