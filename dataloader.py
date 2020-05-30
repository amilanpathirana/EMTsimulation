import elements as el


E1=el.Source("S",0,1,10,0,100.0,0.01)
E2=el.RLC("C",1,2,0.0,0.0,10e-6)
E3=el.RLC("L",1,3,0.0,0.0,10e-6)
E4=el.Switch("R",2,3,0.0,0.0,0.001,100,.1,0)
E5=el.RLC("L",3,0,0.0,0.0,1e-6)

E6=el.Source("S",3,0,1,0,10000.0,0.01)


elemet_list=[E1,E2,E3,E4,E5]


