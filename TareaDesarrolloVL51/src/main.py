from core.VoiceLink import VoiceLink

from vocollect_http.httpserver import server_startup
from httpserver_receiving import ReceivingVoiceAppHTTPServer

# Custom imports
from selection_custom.SelectionPrintCustom import SelectionPrintTask_Custom #@UnusedImport
from vocollect_lut_odr_custom.formattersCustom import RecordFormatter_Custom #@UnusedImport
from selection_custom.PickAssignmentCustom import PickAssignmentTask_Custom #@UnusedImport
from selection_custom.BeginAssignmentCustom import BeginAssignment_Custom #@UnusedImport
from selection_custom.CloseContainerCustom import CloseContainer_Custom#@UnusedImport
from selection_custom.OpenContainerCustom import OpenContainer_Custom #@UnusedImport
from selection_custom.SelectionTaskCustom import SelectionTask_Custom #@UnusedImport
from selection_custom.PickPromptMultipleCustom import PickPromptMultipleTask_Custom #@UnusedImport
from selection_custom.GetAssignmentCustom import GetAssignmentAuto_Custom #@UnusedImport
#Desactivo Desarrollo para estimacion
from selection_custom.SelectionVocabularyCustom import SelectionVocabulary_Custom #@UnusedImport

#dummy ODR to get ODR queue working on startup
from common.VoiceLinkLut import VoiceLinkOdr, lut_def_files
from vocollect_core.utilities.localization import itext
from vocollect_core.utilities import obj_factory
from vocollect_core import scanning
from voice import get_voice_application_property
import voice
from communications.async_http_request import HTTPODRThread
from vocollect_core.utilities.pickler import register_pickle_obj

#Custom luts
lut_def_files.append('LUTDefinition_custom.properties')

def main():
    # load all properties for the currently loaded language
    itext('')

    # Enabling triggered scanning
    use_trigger_scan_vocab = get_voice_application_property('UseTriggerScanVocab')

    voice.log_message("Use Trigger scan vocab value is : "+use_trigger_scan_vocab)
    if use_trigger_scan_vocab == 'true':
        trigger_scan_timeout = int(get_voice_application_property('TriggerScanTimeout'))
        scanning.set_trigger_vocab('VLINK_SCAN_VOCAB')
        scanning.set_trigger_timeout(trigger_scan_timeout)

    server_startup(ReceivingVoiceAppHTTPServer)
    runner = obj_factory.get(VoiceLink)
    runner = register_pickle_obj('VoiceLink', runner)

    # start up the OdrArchive or HTTPODRThread after registering the pickle object
    if get_voice_application_property('useLutOdr') == 'true':
        dummyODR = obj_factory.get(VoiceLinkOdr, 'dummy')
    else:
        HTTPODRThread.start_up()

    runner.execute()

