import elements as el


S1=el.Source("S",0,1,1,0,10000.0,0.01)
B1=el.Branch("C",1,2,0.0,0.0,10e-6)
B2=el.Branch("L",1,3,0.0,0.0,10e-6)
B3=el.Switch("R",2,3,0.0,0.0,0.001,100,.1,0)
B4=el.Branch("L",3,0,0.0,0.0,1e-6)

elemet_list=[B1,B2,S1,B3,B4]

