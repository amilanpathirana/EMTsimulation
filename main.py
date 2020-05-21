import emtcls
import config
import elements as el
            



def run():
    print("Start running the simulation.....")
    Time=config.srtTime
    EMTDC=emtcls.EMT()


    while Time<config.stpTime:
        
        if Time==5*config.Dt:
            el.Switch.togle
            print("Togle")

        EMTDC.formG()
        #print(Time)
        EMTDC.calcBrnHistory(Time)

        EMTDC.calcinjection()

        EMTDC.calcnewV()

        EMTDC.calcNewbranchI()

        EMTDC.recordv(2)
        

        Time=Time+config.Dt

    EMTDC.plotv()
    #print(EMTDC.trace)




if __name__ == "__main__":
    run()