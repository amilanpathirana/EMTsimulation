import elements as el


S1=el.Source("S",0,1,1,0,60.0,1)
B1=el.Branch("C",1,2,0.0,0.0,100e-6)
B2=el.Branch("L",2,3,0.0,0.0,100e-6)
B3=el.Branch("R",3,0,0.0,0.0,10)
B4=el.Branch("L",1,3,0.0,0.0,100e-6)

elemet_list=[S1,B1,B2,B3,B4]