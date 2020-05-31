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
    EMTDC.Vdivide()

    while Time<config.stpTime:

        EMTDC.Vkupdate(Time)        
        EMTDC.calcBrnHistory()
        EMTDC.calcinjection()
        EMTDC.Idivide()
        EMTDC.calIUnew()
        EMTDC.calcnewV()
        EMTDC.reconstruct_V()
        EMTDC.reconstruct_I()
        EMTDC.calcNewbranchI()
        EMTDC.recordv(2)
        Time=Time+config.Dt

    EMTDC.plotv()





if __name__ == "__main__":
    run()