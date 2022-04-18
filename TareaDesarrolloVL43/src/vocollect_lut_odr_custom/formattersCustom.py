'''
Created on 18/11/2020

@author: FranciscoGonzalez
'''
from vocollect_core.utilities import class_factory
from vocollect_lut_odr.formatters import RecordFormatter

class RecordFormatter_Custom(RecordFormatter):
    """A stream-based formatter that separates fields and records, and 
    terminates recordsets.
    
        field_separator - character(s) to seperate fields with
        record_separator - character(s) to terminate a record
        record_set_terminator - character(s) to terminate a record set
    """
    
    #-------------------------------------------------------------------------    
    def __init__(self, field_separator='', 
                 record_separator=chr(10),
                 record_set_terminator=chr(10)):
        self._field_separator = field_separator
        self._record_separator = record_separator
        self._record_set_terminator = record_set_terminator
    
    #-------------------------------------------------------------------------    
    def format_record(self, fields):
        '''Format the record's fields, and terminate with a record separator'''
        from voice import getenv #@UnusedImport
        data = [self.command_name,
#                time.strftime("%m-%d-%y %H:%M:%S"),
#                getenv('Device.Id', ''),
#                getenv('Operator.Id', '')
                ]
        data.extend([str(field) for field in fields])
        #=======================================================================
        # originalmente la funcion va asi: ",".join(data). Pero se quita ',' para que no genere conflicto
        # con desarrollo de sockect independiente a VoiceLink que ejecuta hacia la BD de oracle
        #=======================================================================
        request = "".join(data)
        
        return request + self._record_separator
    
    #-------------------------------------------------------------------------        
    def terminate_recordset(self):
        """Return the end of the record set"""
        return self._record_set_terminator

class_factory.set_override(RecordFormatter, RecordFormatter_Custom)
