'''
Created on 12/11/2020

@author: FranciscoGonzalez
'''
from vocollect_core.utilities import class_factory, obj_factory

from selection.SharedConstants import ENTER_PRINTER, PRINT_LABELS, REPRINT_LABELS, CONFIRM_PRINTER
from common.VoiceLinkLut import VoiceLinkLut
from vocollect_core.dialog.functions import prompt_digits, prompt_only
from vocollect_core.utilities.localization import itext
from core_custom.LutOdr import QuantityBoxesOdr
from selection.SelectionPrint import SelectionPrintTask
import time 
from _voice import print_data, set_print_complete_callback

LABEL_QUANTITIES='label_quantities_to_print'


class SelectionPrintTask_Custom(SelectionPrintTask):

    #-------------------------------------------------------------------------
    def initializeStates(self):
        ''' Initialize States and build LUTs '''
        
        #get printer states
        self.addState(LABEL_QUANTITIES, self.label_quantities)
        self.addState(ENTER_PRINTER, self.enter_printer)
        self.addState(CONFIRM_PRINTER, self.confirm_printer)
        self.addState(PRINT_LABELS, self.print_label)
        self.addState(REPRINT_LABELS, self.reprint_labels)
        
        self._print_lut = obj_factory.get(VoiceLinkLut, 'prTaskLUTPrint')
        self.task = self.taskRunner.findTask(self.name)
        self.dynamic_vocab = None #do not want the selection dynamic vocab

    #-------------------------------------------------------------------------
    def label_quantities(self):
        ''' label_quantities_to_print'''
        self.label_quantities = prompt_digits(itext('ask.for.label.quantities.to.print'), 
                                                            itext('ask.for.label.quantities.to.print.help'), 
                                                            1, 3, 
                                                            True, #Confirm is done in next step for flow purposes 
                                                            False)
        # Ingresa al metodo send_boxex_qty_odr() antes de avanzar al siguiente estado que es ENTER_PRINTER 
        self.send_boxes_qty_odr()
        self.next_state = ENTER_PRINTER
    
    #-------------------------------------------------------------------------        
    def send_boxes_qty_odr(self):
        '''
            Función para enviar ODR con confirmacion de cajas usadas. Se envia un comando
            de actualización para la BD de acuerdo a ID de la asignacion y al valor confirmado.
            Se actualiza el campo de GoalTime que es el valor confirmado por el operador
        '''
        # Genero objeto con clase QuantityBoxesOdr para despues usar el metodo send
        BoxesOdr=QuantityBoxesOdr("UPDATE sel_assignments\
        SET goaltime={0}\
        WHERE assignmentid={1}".format(self.label_quantities, self._assignment['assignmentID']))
        # Se envia con None ya que solo se necesita enviar el comando
        BoxesOdr.send(None)
        # Se deja esperar un tiempo mientras se actualizar el campo goaltime
        time.sleep(2)
        

class_factory.set_override(SelectionPrintTask, SelectionPrintTask_Custom)