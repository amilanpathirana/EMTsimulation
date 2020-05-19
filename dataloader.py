import elements as el


S1=el.Source("S",3,0,10,0,60.0,0.1)
B1=el.Branch("R",1,2,0.0,0.0,1)
B2=el.Branch("L",1,0,0.0,0.0,1e-3)
B3=el.Branch("R",2,3,0.0,0.0,10)
B4=el.Branch("L",1,4,0.0,0.0,1e-3)
B5=el.Branch("C",4,3,0.0,0.0,1e-3)
elemet_list=[S1,B1,B2,B3,B4,B5]