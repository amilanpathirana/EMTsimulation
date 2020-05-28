import emtcls
import config
import elements as el
            



def run():
    print("Start running the simulation.....")
    Time=config.srtTime
    EMTDC=emtcls.Network()


    while Time<config.stpTime:
        
        if Time==5*config.Dt:
            el.Switch.togle
            print("Togle")

        EMTDC.formG()
        EMTDC.Gremake()
        EMTDC.calcBrnHistory(Time)
        EMTDC.calcinjection()
        EMTDC.calcnewV()
        EMTDC.calcNewbranchI()
        EMTDC.recordv(2)
        
        Time=Time+config.Dt

    EMTDC.plotv()





if __name__ == "__main__":
    run()