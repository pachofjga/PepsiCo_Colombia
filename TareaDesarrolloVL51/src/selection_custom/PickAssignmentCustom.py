'''
Created on 26/12/2020

@author: FranciscoGonzalez
'''
from vocollect_core.utilities import class_factory
from selection.PickAssignment import PickAssignmentTask
from vocollect_core.utilities.localization import itext
from vocollect_core.dialog.functions import prompt_ready
from selection_custom.PickingAndPassCustom import PickingAndPass as PAP
from selection.SharedConstants import PICK_ASSIGNMENT_AISLE,\
    PICK_ASSIGNMENT_CHECK_NEXT_PICK
from common.VoiceLinkLut import VoiceLinkLut

class PickAssignmentTask_Custom(PickAssignmentTask):
    
    #----------------------------------------------------------     
    def pre_aisle(self):
        ''' directing to Pre Aisle'''
        #FraGon 26122002 Se quita dialogo de preAisle porque no se va a usar y se ocupa el campo para picking por zonas 
        if self._pickList[0]["preAisle"] != self._pre_aisle_direction:
            if self._pickList[0]["preAisle"] != '':
                pass

            self._post_aisle_direction=''
            self._aisle_direction=''
            self._pre_aisle_direction = self._pickList[0]["preAisle"]
            
    #----------------------------------------------------------
    def aisle(self):
        ''' directing to Aisle'''
        #if aisle is same as aisle don't prompt
        #FraGon 27032021 Se quita dialogo de aisle porque no se va a usar en picking por zonas
        pickingandpass=PAP()
        if (pickingandpass.isLUTEmpty()):
            lut = VoiceLinkLut('prTaskLUTCustomCheckForPrint')
            lut.do_transmit(self._assignment_lut[0]['assignmentID'])
            #islast_lut= VoiceLinkLut('prTaskLUTCustomCheckForLast')
            #islast_lut.do_transmit(self._assignment_lut[0]['assignmentID'])
            PAP(lut)        
        if not pickingandpass.isAsgDev():
            result = ''
            if self._pickList[0]["aisle"] != self._aisle_direction:
                if self._pickList[0]["aisle"] != '':
                    result = prompt_ready(itext('selection.pick.assignment.aisle', 
                                                     self._pickList[0]["aisle"]), True,
                                                     {'skip aisle' : False})
                    if result == 'skip aisle':
                        self.next_state = PICK_ASSIGNMENT_AISLE
                        self._skip_aisle()
    
                if result != 'skip aisle':
                    self._post_aisle_direction=''
                    self._aisle_direction = self._pickList[0]["aisle"]
                    
    #----------------------------------------------------------        
    def end_picking(self):
        ''' End Picking'''
        #end picking
        if self.status == 'B':
            self.status = 'N'
            self.next_state = PICK_ASSIGNMENT_CHECK_NEXT_PICK
            self._update_status('', 2, 'N')
        elif self.status == 'N':
            if not self._region['pickByPick']:
                if self._picks_lut.has_picks(None, ['N', 'S']):
                    for pick in self._picks_lut:
                        if pick['status'] == 'S':
                            pick['status'] = 'N'
                    self.next_state = PICK_ASSIGNMENT_CHECK_NEXT_PICK
                    self._update_status('', 2, 'N')
                else:
                    #prompt_only(itext('selection.pick.assignment.picking.complete'))
                    pass    
        else:
            self.dynamic_vocab.next_pick([])
            


class_factory.set_override(PickAssignmentTask, PickAssignmentTask_Custom)