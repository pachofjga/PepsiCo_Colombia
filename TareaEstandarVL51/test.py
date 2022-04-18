import mock_catalyst
from mock_catalyst import EndOfApplication
from vocollect_lut_odr_test.mock_server import MockServer, BOTH_SERVERS
from main import main
import sys

mock_catalyst.environment_properties['SwVersion.Locale'] = 'es_MX'
mock_catalyst.environment_properties['Operator.Id'] = '1018447946'
mock_catalyst.environment_properties['Operator.Name'] = 'Francisco Gonzalez'

#create a simulated host server
#ms = MockServer(use_std_in_out = True)
#ms.start_server(BOTH_SERVERS)
#ms.set_pass_through_host('127.0.0.1', 15004, 15005)
#ms.load_server_responses("Test/voicelink_test/Data/test1.xml")
#ms.set_server_response('Y', 'prTaskODR')

#===============================================================================
# VER LOG DE TAREAS EN ARTISAN, SE COLOCA EN EL TEST.PY
#===============================================================================
def log_message(msg):
     if mock_catalyst.use_stdin_stdout:
         sys.stdout.write('>> ' + msg + '\n')
         sys.stdout.flush()
    
sys.modules['voice'].log_message = log_message
  
#Post responses
mock_catalyst.post_dialog_responses('ready',
                                  '123!')

try:
    main()
except EndOfApplication as err:
    print('Application ended')
    
#ms.stop_server(BOTH_SERVERS)


#Sample test case creation
#from CreateTestFile import CreateTestFile
#test = CreateTestFile('Sample', ms)
#path = '' #should end with slash if specified (i.e. test\functional_tests\Selection_tests\)
#test.write_test_to_file(path)
