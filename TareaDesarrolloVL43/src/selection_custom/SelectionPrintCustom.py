'''
Created on 12/11/2020

@author: FranciscoGonzalez
'''
from vocollect_core.utilities import class_factory, obj_factory

from selection.SharedConstants import ENTER_PRINTER, PRINT_LABELS, REPRINT_LABELS, CONFIRM_PRINTER
from common.VoiceLinkLut import VoiceLinkLut
from vocollect_core.dialog.functions import prompt_digits
from vocollect_core.utilities.localization import itext
from core_custom.LutOdr import QuantityBoxesOdr
from selection.SelectionPrint import SelectionPrintTask
from selection_custom.CreateVirtualContainer import VirtualContainer as VC
from selection_custom.PickingAndPassCustom import PickingAndPass as PAP
import time 

LABEL_QUANTITIES='label_quantities_to_print'
CHECK_FOR_PRINT='checkForPrint'
class SelectionPrintTask_Custom(SelectionPrintTask):

    #-------------------------------------------------------------------------
    def initializeStates(self):
        ''' Initialize States and build LUTs '''
        #get printer states
        self.addState(CHECK_FOR_PRINT, self.check_for_print)
        self.addState(LABEL_QUANTITIES, self.label_quantities)
        self.addState(ENTER_PRINTER, self.enter_printer)
        self.addState(CONFIRM_PRINTER, self.confirm_printer)
        self.addState(PRINT_LABELS, self.print_label)
        self.addState(REPRINT_LABELS, self.reprint_labels)
        self._print_lut = obj_factory.get(VoiceLinkLut, 'prTaskLUTPrint')
        self.task = self.taskRunner.findTask(self.name)
        self.dynamic_vocab = None #do not want the selection dynamic vocab
    #-------------------------------------------------------------------------
    #JDominguez add custom state
    def check_for_print(self):
        self._print_assignmnent = None
        pickingandpass=PAP()
        if (pickingandpass.isLUTEmpty()):
            lut = VoiceLinkLut('prTaskLUTCustomCheckForPrint')
            lut.do_transmit(self._assignment['assignmentID'])
            islast_lut = VoiceLinkLut('prTaskLUTCustomCheckForLast')
            islast_lut.do_transmit(self._assignment['assignmentID'])
            PAP(lut,islast_lut)
        #Pregunta si asignacion es de tipo split
        if (pickingandpass.isAsgDev()) and not(pickingandpass.isPallet()):
            contenedor=VC()
            #FraGon 25022021 Pregunta si etiqueta ya ha sido impresa y preguntar por nuevos contenedores
            if (pickingandpass.isPrinted()) and (contenedor.get_container_count()==1):
                self.next_state = ''
            elif (pickingandpass.isPrinted()) and (contenedor.get_container_count()>1):
                self.next_state = ENTER_PRINTER                
            else:
                self.next_state = ENTER_PRINTER
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
        
    #-------------------------------------------------------------------------
    def print_label(self):
        ''' print labels'''
        #FraGon 19Febrero2021 se agrega logica para nuevo contenedor cuando son asignaciones de tipo split
        contenedor=VC()
        container=contenedor.get_container_number()
        pickingandpass=PAP()
        if (pickingandpass.isLUTEmpty()):
            lut = VoiceLinkLut('prTaskLUTCustomCheckForPrint')
            lut.do_transmit(self._assignment['assignmentID'])
            islast_lut = VoiceLinkLut('prTaskLUTCustomCheckForLast')
            islast_lut.do_transmit(self._assignment['assignmentID'])
            PAP(lut,islast_lut)
        #if reprint labels is not set
        if not self._reprint_label:
            assignment_id = self._assignment['assignmentID']
            if self._region['containerType'] == 0 and self._assignment.parent.has_multiple_assignments():
                assignment_id= ''
            if (pickingandpass.isPrinted()) and (contenedor.get_container_count()==1):                    
                result = self._print_lut.do_transmit(self._assignment['groupID'], assignment_id,
                                                 self.operation, '', self.task.printer_number, self._reprint_label)
            elif (pickingandpass.isPrinted()) and (contenedor.get_container_count()>1):
                result = self._print_lut.do_transmit(self._assignment['groupID'], assignment_id,
                                                 self.operation, container, self.task.printer_number, self._reprint_label)
            else:    
                result = self._print_lut.do_transmit(self._assignment['groupID'], assignment_id,
                                                 self.operation, '', self.task.printer_number, self._reprint_label)
                
                
            if result < 0:
                self.next_state = PRINT_LABELS
            elif result > 0:
                self.next_state = ENTER_PRINTER
            else:
                self.next_state = ''
        else:
            self.next_state = REPRINT_LABELS 
            
    #-------------------------------------------------------------------------
    def enter_printer(self):
        if not hasattr(self.task, 'printer_number') or self.task.printer_number is None:
            self.task.printer_number = prompt_digits(itext('generic.printer'), 
                                                            itext('generic.printer.help'), 
                                                            1, 2, 
                                                            False, #Confirm is done in next step for flow purposes 
                                                            False)
        else:
            #27032021 FraGon Se agrega condicion para saltar confirmacion
            self.next_state = PRINT_LABELS

class_factory.set_override(SelectionPrintTask, SelectionPrintTask_Custom)