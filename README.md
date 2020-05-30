___


# DommelSim
___
Free EMT simulation program based on Domels algorithm
---
## Steps of the DommelSim algorithm
1. Generate the conductance matrix G
2. Divide the G into Guu,Guk,Gku,Gkk
3. Use LU decompossition and obtain upper triangular matrix of Guu
4. Initialize IU,IK,VU and VK

####Enter main time loop
5.  Update voltage sources
6.  Calculate the history currents of all the branches(ihistory)
7.  Calculate the current injection (IH)
8.  Divide the IH into IU and IK
9.  Calculate IUnew (IUnew=IU-Guk*Vk)
10. Calculate node voltages(VU)
11. Reconstruct Vn (concat VU and VK)
12. 


###Sample program
```python
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
        EMTDC.recordv(3)
        
        Time=Time+config.Dt

    EMTDC.plotv()
```


[Amila Pathirana](www.apathirana.com)
