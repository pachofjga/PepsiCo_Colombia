'''
Created on 2/03/2021

@author: FranciscoGonzalez
'''
from vocollect_core.utilities import class_factory
from common.VoiceLinkLut import VoiceLinkLut
from selection.SelectionTask import SelectionTask
from selection.SharedConstants import REGIONS, COMPLETE_ASSIGNMENT
from selection_custom.PickingAndPassCustom import PickingAndPass as PAP


class SelectionTask_Custom(SelectionTask):
    
    #----------------------------------------------------------
    def complete_assignment(self):
        '''Complete assignment'''
        #check if any passed assignments
        passed = False
        self.set_sign_off_allowed(True)
        
        for assignment in self._assignment_lut:
            if assignment['passAssignment'] == '1' and self.dynamic_vocab._pass_inprogress:
                passed = True
                        
        # Send LUT telling server the assignment is complete.
        self.dynamic_vocab.clear()
        result = 0
        if passed:
            result = self._pass_assignment_lut.do_transmit(self._assignment_lut[0]['groupID'])
        else:
            result = self._stop_assignment_lut.do_transmit(self._assignment_lut[0]['groupID'])
            
        if result == 2:
            # Special case return code tells the operator to switch regions
            self.next_state = REGIONS
        elif result < 0 or result > 0:
            # Failure to send LUT, retry this state
            self.next_state = COMPLETE_ASSIGNMENT
        else:
            if passed:
                self._assignment_complete_prompt_key = 'selection.pass.assignment.confirm'
            else:
                #FraGon 02032021 Pregunta si asignacion es de desarrollos en VLINK
                pickingandpass=PAP()
                if (pickingandpass.isLUTEmpty()):
                    lut = VoiceLinkLut('prTaskLUTCustomCheckForPrint')
                    lut.do_transmit(self._assignment_lut[0]['assignmentID'])
                    islast_lut = VoiceLinkLut('prTaskLUTCustomCheckForLast')
                    islast_lut.do_transmit(self._assignment_lut[0]['assignmentID'])
                    PAP(lut,islast_lut)
                if (pickingandpass.isSplitted()):
                    #FraGon 02032021 Confirma si asignacion se cierra para la zona donde pasa la caja o continua
                    #print("es ultima caja:", pickingandpass.isLast())
                    if pickingandpass.isLast():
                        self._assignment_complete_prompt_key ='selection.complete.assignment.confirm.custom.last'
                    else:
                        self._assignment_complete_prompt_key ='selection.complete.assignment.confirm.custom.nolast'
                else:
                    self._assignment_complete_prompt_key = 'selection.complete.assignment.confirm'

            self.dynamic_vocab.next_pick([])

class_factory.set_override(SelectionTask, SelectionTask_Custom)