'''
Created on 17/02/2021

@author: FranciscoGonzalez
'''
class VirtualContainer:
    ''' Clase que almacena la informacion de contenedores abiertos'''
    containercount=0
    containernumber=0
    def __init__(self, container=None):
        '''Si no se envia LUT no se guarda informacion de numero de contenedores abiertos'''
        if (container is not None):
            VirtualContainer.containercount=len(container)
            #print("Cuenta de contenedores: {0} y contenedor actual: {1}".format(VirtualContainer.containercount, container[0]['systemContainerID']))
            VirtualContainer.containernumber=container[0]['systemContainerID']
                               
    def get_container_count(self):
        #FraGon 25022021 Devuelve el numero de contenedores abiertos
        print()
        return VirtualContainer.containercount
    
    
    def get_container_number(self):
        #FraGon devuelve el numero de contenedor que esta actualmente abierto
        return VirtualContainer.containernumber
    
    
        
    
