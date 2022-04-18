'''
Created on 12/11/2020

@author: FranciscoGonzalez
'''
from vocollect_core.utilities import class_factory, obj_factory
#from selection.SharedConstants import ENTER_PRINTER, PRINT_LABELS, REPRINT_LABELS, CONFIRM_PRINTER
from common.VoiceLinkLut import VoiceLinkLut
from vocollect_core.dialog.functions import prompt_digits, prompt_yes_no
from vocollect_core.utilities.localization import itext
from core_custom.LutOdr import QuantityBoxesOdr
from selection.SelectionPrint import SelectionPrintTask
import time
from datetime import datetime
from voice import getenv
from _voice import print_data

LABEL_QUANTITIES='label_quantities_to_print'
ENTER_PRINTER_BT='Bluetooth_printer'
ENTER_PRINTER_CUSTOM='Enter_printer_custom'
CONFIRM_PRINTER_CUSTOM='Confirm_printer_custom'



class SelectionPrintTask_Custom(SelectionPrintTask):

    #-------------------------------------------------------------------------
    def initializeStates(self):
        ''' Initialize States and build LUTs '''
        
        #get printer states
        self.addState(LABEL_QUANTITIES, self.label_quantities)
        self.addState(ENTER_PRINTER_BT, self.enter_printer_bt)        
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
        self.next_state = ENTER_PRINTER_BT
    
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
    def enter_printer_bt(self):
        if prompt_yes_no(itext('ask.for.printer.type')):
            self.print_by_bluetooth()
        else:
            self.addState(ENTER_PRINTER_CUSTOM, self.enter_printer_custom)
            self.addState(CONFIRM_PRINTER_CUSTOM, self.confirm_printer_custom)
            self.next_state=ENTER_PRINTER_CUSTOM
                
    #-------------------------------------------------------------------------
    def print_by_bluetooth(self):
        etiqueta="^XA~TA000~JSN^LT0^MMT^MNW^MTT^PON^PMN^LH0,0^JMA^PR4,4^MD0^JUS^LRN^CI0^XZ\
        DATA_BODY>^XA^LL1200\
        ^LS0\
        ^FT40,90^A0N,45,45^FH\\^FDCOMERCIALIZADORA NACIONAL SAS Ltda^FS\
        ^FT40,180^A0,32,32^FH\\^FDSEDE: {0}^FS\
        ^FT440,180^A0,32,32^FH\\^FDFECHA: {1}^FS\
        ^FT40,250^A0,32,32^FH\\^FDCLIENTE: {2}^FS\
        ^FT40,320^A0,32,32^FH\\^FDDIRECCION DE ENVIO: {3}^FS\
        ^FT40,390^A0,32,32^FH\\^FDORDEN INTERNA: {4}^FS\
        ^FT460,390^A0,32,32^FH\\^FDRUTA: ^FS\
        ^FT550,390^A0,60,60^FH\\^FD{5}^FS\
        ^FT40,460^A0,32,32^FH\\^FDORDEN DEL CLIENTE #: {6}^FS\
        ^FT40,530^A0,32,32^FH\\^FDPICKER: {7}^FS\
        ^FT440,530^A0,32,32^FH\\^FD{8}^FS\
        ^FT650,530^A0,32,32^SN01,1,N ^FS\
        ^FT680,530^A0,32,32^FH\\^FDDE {9}^FS\
        ^PQ{10},0,0,Y^XZ\
        </DATA_BODY>".format("#Nombre Region", datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                             "#Nombre de cliente", "#Direccion de envio", self._assignment['idDescription'],
                             self._assignment['route'], "# de orden", getenv('Operator.Name', ''),
                             "# Cliente", self.label_quantities, self.label_quantities)
        print_data(etiqueta, 65001)
        self.validate_label_printed()
    
    #-------------------------------------------------------------------------
    def validate_label_printed(self):
        if prompt_yes_no(itext('ask.for.print.action')):
            self.next_state = ''
        else:
            self.addState(ENTER_PRINTER_CUSTOM, self.enter_printer_custom)
            self.addState(CONFIRM_PRINTER_CUSTOM, self.confirm_printer_custom)
            self.next_state=ENTER_PRINTER_CUSTOM
                    
    #-------------------------------------------------------------------------
    def enter_printer_custom(self):
        if not hasattr(self.task, 'printer_number') or self.task.printer_number is None:
            self.task.printer_number = prompt_digits(itext('generic.printer'), 
                                                            itext('generic.printer.help'), 
                                                            1, 2, 
                                                            False, #Confirm is done in next step for flow purposes 
                                                            False)
            self.next_state=CONFIRM_PRINTER_CUSTOM
        

    #-------------------------------------------------------------------------
    def confirm_printer_custom(self):
        if not prompt_yes_no(itext('generic.printer.confirm', 
                                        self.task.printer_number), True):
            self.task.printer_number = None
            self.next_state = ENTER_PRINTER_CUSTOM

class_factory.set_override(SelectionPrintTask, SelectionPrintTask_Custom)