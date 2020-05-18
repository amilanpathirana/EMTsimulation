import numpy as np
import config
class EMT:
    def __init__(self):
        self.comp_list = [] 
        self.S1=Source("S",3,0,10,0,60.0,0.1)
        # appending elements to list  
        self.comp_list.append(Branch("R",1,2,0.0,0.0,1)) 
        self.comp_list.append(Branch("L",1,0,0.0,0.0,1e-3)) 
        self.comp_list.append(self.S1) 
        self.comp_list.append(Branch("R",2,3,0.0,0.0,10))

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


    # Initialize [G] matrix to zero
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

        #test whether series and prellel
        for obj in self.comp_list:
            print(obj.brnType,obj.Series)
        
        


    """def kronR(self):
        for obj in self.list:
            Type = obj.brnType
            if Type=="S":
                k=obj.stpnode
        print(self.G)
        for i in range(self.numNodes):
            for j in range(self.numNodes):
                print(i,j)
                self.G[i][j]= self.G[i][j]- (self.G[i][k]*self.G[k][j])/self.G[k][k]
        

        self.Gk=np.delete(self.G,self.numNodes-1,0)
        self.Gk=np.delete(self.Gk,self.numNodes-1,1)

        print(self.Gk)"""


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

    def updateVol(self):
        for obj in self.comp_list:
            Type = obj.brnType
            From = obj.strnode-1
            To = obj.stpnode-1
            self.I_History_src[2] = self.S1.Sourceupdate(TheTime)
       
        self.I_History=np.add(self.I_History,self.I_History_src)
        

        
            
            




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

class Source():
    def __init__(self,brnType,strnode,stpnode,magnitude,angle,frequency,value):
        self.brnType = brnType
        self.strnode= strnode
        self.stpnode= stpnode
        self.magnitude= magnitude
        self.angle= angle
        self.frequency= frequency
        self.Reff=value
    def Sourceupdate(self,TheTime):
        V_mag = self.magnitude
        V_ang = self.angle
        freq = self.frequency
        V_instantaneous = V_mag*np.sin(2.0*np.pi*50.0*TheTime + V_ang*np.pi/180.0)
        return V_instantaneous

 



#Initialize G with 4X4
print("Create EMT object")
EMTDC=EMT()
# Add componets and form G matrix
print("Form G")
EMTDC.formG()

# go to net timestep
TheTime=-0.0123
#Update Sources
EMTDC.updateVol()

print("Calc Branch current history")
EMTDC.calcBrnHistory()


print("Calc current injection")

EMTDC.calcinjection()

EMTDC.calcnewV()





# Update sources

# Calculate history









