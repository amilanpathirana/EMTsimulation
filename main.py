import emtcls
import config
import elements as el
            



def run():
    print("Start running the simulation..... \n")
    Time=config.srtTime
    EMTDC=emtcls.Network()
    EMTDC.formG()
    EMTDC.Gremake()

    while Time<config.stpTime:
        
        EMTDC.calcBrnHistory(Time)
        EMTDC.calcinjection()
        EMTDC.calcnewV()
        EMTDC.calcNewbranchI()
        EMTDC.recordv(3)
        
        Time=Time+config.Dt

    EMTDC.plotv()





if __name__ == "__main__":
    run()