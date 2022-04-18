'''
Created on 9/01/2021

@author: FranciscoGonzalez
'''
from vocollect_core.utilities import class_factory
from selection.OpenContainer import OpenContainer
from vocollect_core.utilities.localization import itext
from selection.SharedConstants import OPEN_CONTAINER_OPEN
from vocollect_core.dialog.functions import prompt_alpha_numeric, prompt_ready #@UnusedImport
from selection_custom.CreateVirtualContainer import VirtualContainer as VC

class OpenContainer_Custom(OpenContainer):
    
    #----------------------------------------------------------
    def open_container(self):
        container=''
        
        if self._position == '':
            prompt = itext('selection.new.container.prompt.for.container.id')
        else:
            prompt = itext('selection.new.container.prompt.for.container', self._position)
           
        if self._region['promptForContainer'] == 1:
            result = prompt_alpha_numeric(prompt, 
                                          itext('selection.new.container.prompt.for.container.help'), 
                                          confirm=True,scan=True)
            container = result[0]
            
        result = -1
        if self._picks[0]['targetContainer'] == 0:
            target_container = ''
        else:
            target_container = self._picks[0]['targetContainer']
            
        while result < 0:
            result = self._container_lut.do_transmit(self._assignment['groupID'], 
                                                     self._assignment['assignmentID'], target_container, '', container, 2 , '')
        
        if result > 0:
            self.next_state = OPEN_CONTAINER_OPEN
            
        if result == 0:
            if self._region['promptForContainer'] != 1:
                if self._position == '':
                    prompt_last = itext('selection.new.container.prompt.open.last', self._container_lut[0]['spokenValidation']) #@UnusedVariable
                    if self._picks[0]['targetContainer'] != 0:
                        self._assignment['activeTargetContainer'] = self._container_lut[0]['targetConatiner']
                else:
                    containers = self._container_lut.get_open_containers(self._assignment['assignmentID'])
                    if len(containers) == 0:
                        containers = self._container_lut.get_closed_containers(self._assignment['assignmentID'])
                    if len(containers) > 0:    
                        prompt_last = itext('selection.new.container.prompt.open.last.multiple', #@UnusedVariable
                                          containers[0]['spokenValidation'], 
                                             self._position)
                    else:
                        prompt_last = itext('selection.new.container.no.containers.returned') #@UnusedVariable
                #FraGon 09012021 Se salta este prompt para no mostrar mensaje abra                        
                #prompt_ready(prompt_last)
                #print("Numero de contenedor: ", self._container_lut[0])
                #FraGon 25022021 Guardo contenedor que se abra a enviando la LUT
                contenedor=VC(self._container_lut) #@UnusedVariable
            
            if self._region['printLabels'] == '1':
                if  self._container_lut[0]['printed']  == 0:
                    self._print_label()
    
    
    pass

class_factory.set_override(OpenContainer, OpenContainer_Custom)