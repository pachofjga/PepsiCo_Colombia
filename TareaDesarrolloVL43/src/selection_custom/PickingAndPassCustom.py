'''
Created on 25/05/2021

@author: FranciscoGonzalez
'''
class PickingAndPass:
    PickingAndPastLUT=None
    CheckForLastLUT=None
    
    def __init__(self, PickingPassLUT=None, check4lastLUT=None):
        #FraGon 25052021 Se almacenan LUTS para retornar validaciones posteriores
        if (PickingPassLUT is not None):
            PickingAndPass.PickingAndPastLUT=PickingPassLUT
        if (check4lastLUT is not None):
            PickingAndPass.CheckForLastLUT=check4lastLUT
        
    def isLUTEmpty(self):
        if (PickingAndPass.PickingAndPastLUT is None) and (PickingAndPass.CheckForLastLUT is None):
            #print("Esta Vacia la LUT")
            return True
        return False            
        
    def isPrinted(self):
        #FraGon 25052021 Retorna True si la etiqueta ya ha sido impresa
        #print("Is printed", self.PickingAndPastLUT[0]['isPrinted']=="1")
        return True if self.PickingAndPastLUT[0]['isPrinted']=="1" else False
       
    def isAsgDev(self):
        #FraGon 25052021 Retorna True si la asignacion es desarrollada en VLINK
        #print("Is dev", self.PickingAndPastLUT[0]['assignmentID']!="0")
        return True if self.PickingAndPastLUT[0]['assignmentID']!="0" else False
    
    def isSplitted(self):
        #FraGon 25052021 Retorna True si la assignacion fue calculada para Picking por zonas
        #print("Is splitted", self.PickingAndPastLUT[0]['assignmentID']=="1")
        return True if self.PickingAndPastLUT[0]['assignmentID']=="1" else False
    
    def isBox(self):
        #FraGon 25052021 Retorna True si la assignacion es de picking por zonas unidad de medida cajas
        #print("Is box", self.PickingAndPastLUT[0]['assignmentID']=="2")
        return True if self.PickingAndPastLUT[0]['assignmentID']=="2" else False
    
    def isPallet(self):
        #FraGon 25052021 Retorna True si la assignacion es de picking por zonas unidad de medida pallet
        #print("Is pallet", self.PickingAndPastLUT[0]['assignmentID']=="3")
        return True if self.PickingAndPastLUT[0]['assignmentID']=="3" else False
    
    def isLast(self):
        #FraGon 25052021 Retorna True si la caja pasa a banda de lo contrario pasa a zona.
        #print("Is last", self.CheckForLastLUT[0]['isLast']=='1')
        return True if self.CheckForLastLUT[0]['isLast']=='1' else False
    
    