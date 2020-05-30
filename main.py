import emtcls
import config
import elements as el
import dataloader as dl
            

def run():
    print("\nStart running the simulation..... \n")
    Time=config.srtTime

    EMTDC=emtcls.Network()
    EMTDC.formG()
    EMTDC.Gdivide()
    EMTDC.LU()

    while Time<config.stpTime:
        
        EMTDC.IVdevide()
        EMTDC.calcBrnHistory(Time)
        EMTDC.calcinjection()
        EMTDC.calcnewV()
        EMTDC.reconstruct_V()
        EMTDC.reconstruct_I()
        EMTDC.calcNewbranchI()
        EMTDC.recordv(2)
        
        Time=Time+config.Dt

    EMTDC.plotv()





if __name__ == "__main__":
    run()