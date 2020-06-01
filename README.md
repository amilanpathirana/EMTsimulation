___


# DommelSim by Amila Pathirana
___
Free EMT simulation program based on Domels algorithm
---
## Steps of the simulation algorithm inside DommelSim
__
1. Generate the conductance matrix G
2. Divide the G into Guu,Guk,Gku,Gkk
3. Use LU decompossition and obtain upper triangular matrix of Guu
4. Initialize IU,IK,VU and VK
5. Enter main time loop
6. Update voltage sources
8. Calculate the history currents of all the branches(ihistory)
9. Calculate the current injection (IH)
10. Divide the IH into IU and IK
11. Calculate IUnew (IUnew=IU-Guk*Vk)
12. Calculate node voltages(VU)
13. Reconstruct Vn (concat VU and VK)
    
___

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
_____

[Amila Pathirana](http://www.apathirana.com)
