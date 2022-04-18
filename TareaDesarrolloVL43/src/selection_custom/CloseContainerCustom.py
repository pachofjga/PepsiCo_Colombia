'''
Created on 8/01/2021

@author: FranciscoGonzalez
'''
from vocollect_core.utilities import class_factory, obj_factory
from selection.CloseContainer import CloseContainer
from selection.SelectionPrint import SelectionPrintTask
from common.VoiceLinkLut import VoiceLinkLut
from selection_custom.CreateVirtualContainer import VirtualContainer as VC
from selection_custom.PickingAndPassCustom import PickingAndPass as PAP

class CloseContainer_Custom(CloseContainer):
    
    #----------------------------------------------------------
    def print_label(self):
        ''' Print labels if region print label is set'''
        if self._region['printLabels'] == '2':
            #FraGon 08012021 Pregunto si el desarrollo esta activo para imprimir etiqueta
            #SelectionPrintTask que es sobreescrita por SelectionPrintTask_Custom se direcciona a clase diferente que puede imprimir
            pickingandpass=PAP()
            if (pickingandpass.isLUTEmpty()):
                lut = VoiceLinkLut('prTaskLUTCustomCheckForPrint')
                lut.do_transmit(self._assignment_lut[0]['assignmentID'])
                islast_lut = VoiceLinkLut('prTaskLUTCustomCheckForLast')
                islast_lut.do_transmit(self._assignment_lut[0]['assignmentID'])
                pickingandpass=PAP(lut,islast_lut)       
            #Pregunta si asignacion es de tipo split de unidades y piezas
            if pickingandpass.isSplitted():
                # Pregunto si la etiqueta ha sido impresa, caso busca caja
                if pickingandpass.isPrinted():
                    contenedor = VC()
                    #Para el caso de buscar caja no se debe imprimir la primera vez
                    if contenedor.get_container_count()>1:
                        self.launch(obj_factory.get(SelectionPrintTask,self._region,
                                                  self._assignment,
                                                  self._container_lut,
                                                  0,
                                                  self.taskRunner,
                                                  self))                     
                else:
                    self.launch(SelectionPrintTask(self._region,
                                                  self._assignment,
                                                  self._container_lut,
                                                  0,
                                                  self.taskRunner,
                                                  self))
            else:
                if  self._container['printed']  == 0:
                    self.launch(obj_factory.get(SelectionPrintTask,
                                                  self._region, 
                                                  self._assignment,  
                                                  self._container_lut, 
                                                  0, 
                                                  self.taskRunner, self))

class_factory.set_override(CloseContainer, CloseContainer_Custom)