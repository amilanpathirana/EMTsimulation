import elements as el


#E1=el.Source("S",0,1,10,0,100.0,0.01)
E2=el.RLC("R",1,2,0.0,0.0,1)
E3=el.RLC("C",2,3,0.0,0.0,0.5e-6)
#E4=el.Switch("R",1,2,0.0,0.0,0.001,1000,.1,0)
E5=el.RLC("L",0,1,0.0,0.0,500e-6)
E6=el.Source("S",3,0,1,12,10.0,1)


elemet_list=[E2,E3,E5,E6] 


