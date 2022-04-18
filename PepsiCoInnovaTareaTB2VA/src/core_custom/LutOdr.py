'''
Created on 18/11/2020

@author: FranciscoGonzalez

Esta libreria permite el manejo de luts y odr de VoiceLink
Se usa unicamente la clase QuantityBoxesOdr para trabajar con
un servicio externo que ejecuta un comando en la BD de Oracle
'''

from voice import get_voice_application_property
import time

# import from vocollect LUT ODR core library
from vocollect_lut_odr.connections import LutConnection, OdrConnection
from vocollect_lut_odr.receivers import Lut, OdrConfirmationByte #@UnusedImport
from vocollect_lut_odr.transports import TransientSocketTransport

from vocollect_core.dialog.functions import prompt_yes_no, prompt_only, prompt_ready, prompt_digits #@UnusedImport
from vocollect_lut_odr_custom.formattersCustom import RecordFormatter_Custom

class QuantityBoxesOdr(object):
    
    def __init__(self, command, *fields):
        # create the transport
        self._transport = TransientSocketTransport(
                        str(get_voice_application_property('BoxHost')),
                        int(get_voice_application_property('BoxODR')))
        # Se genera objeto de la clase RecordFormatter_Custom() en vacio porque no se necesita separacion de campos
        # Se enviara un comando para ejecutar por Oracle
        self._formatter = RecordFormatter_Custom('')
       
        #=======================================================================
        # OdrConnection('BoxexQuantityODR', self._transport,self._formatter, OdrConfirmationByte(), auto_transmit=True)
        # Se coloca en el campo OdrConfirmationByte() para que la terminal no se quede enviando el ODR y esperando
        # información de retorno ya que el servicio no retonar un valor de confirmación
        #=======================================================================
        
        self._connection = OdrConnection('BoxexQuantityODR', self._transport,
                                self._formatter, None, auto_transmit=True)
        self._command=command
                
    def send(self, *fields):
        # save the command
        self._formatter.command_name =  self._command
        
        # insure all fields have a value
        field_list = [x if x is not None else '' for x in fields]
        
        #sent the ODR
        self._connection.append(field_list)
        
                
    
class QuantityBoxesLut(object):
    
    def __init__(self, command, *fields):
        #create the transport
        self._transport = TransientSocketTransport(
                                                   str(get_voice_application_property('BoxHost')),
                                                   int(get_voice_application_property('BoxODR')))
        
        #define the lut
        self._connection = LutConnection(self._transport,
                                         RecordFormatter_Custom(command),
                                         Lut(*fields))
        
    def send(self, *fields):
        #insure all fields have a value
        field_list = [x if x is not None else '' for x in fields]

        error = -1
        try:
            #Transmit and wait for response
            self._connection.append(field_list)
            
            #Check for data every 20ms, and beep every 2
            #seconds to let user now we are still waiting
            start = time.clock()
            while not self._connection.data_ready():
                time.sleep(0.02)
                now = time.clock()
                if now - start > 2:
                    start = now
                    import voice
                    voice.audio.beep(400, 0.2)
            error = 0
            
        except Exception:
            pass
#            prompt_ready('Error',True)
        return error
    
    def getdata(self):
        return self._connection.lut_data  
        