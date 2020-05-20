import elements as el


S1=el.Source("S",0,1,10,0,600.0,0.1)
B1=el.Branch("C",1,2,0.0,0.0,1000e-3)
B2=el.Branch("L",2,3,0.0,0.0,1000e-3)
B3=el.Branch("R",3,0,0.0,0.0,10)


elemet_list=[S1,B1,B2,B3]