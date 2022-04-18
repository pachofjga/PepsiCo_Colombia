'''
Created on 26/12/2020

@author: FranciscoGonzalez
'''
from vocollect_core.utilities import class_factory
from selection.BeginAssignment import BeginAssignment
from vocollect_core.utilities.localization import itext
from vocollect_core.dialog.functions import prompt_ready
from common.VoiceLinkLut import VoiceLinkLut
from selection_custom.PickingAndPassCustom import PickingAndPass as PAP



class BeginAssignment_Custom(BeginAssignment):
    #----------------------------------------------------------    
    def summmary_prompt(self):
        ''' speak the summary prompt for all the assignments '''
        #FraGon 06012021 Utilizo lut de impresion para generar dialogo adicional de caja nueva o caja media
        # y cambiar prompt de bienvenida
        pickingandpass=PAP()
        if (pickingandpass.isLUTEmpty()):
                lut = VoiceLinkLut('prTaskLUTCustomCheckForPrint')
                lut.do_transmit(self._assignment_lut[0]['assignmentID'])
                #02112021 FraGon Se comenta isLastLut por unificacion de LUTs desarrolladas
                #islast_lut = VoiceLinkLut('prTaskLUTCustomCheckForLast')
                #islast_lut.do_transmit(self._assignment_lut[0]['assignmentID'])
                pickingandpass=PAP(lut)        
        #FraGon 06012021 Pregunta si asignacion es de tipo split
        if pickingandpass.isAsgDev():
            pass
            #===================================================================
            # SE COMENTA PORQUE SE COLOCA EN GET ASSIGNMENT CUSTOM ANTE DEL PICK REVERSE
            #===================================================================
            #===================================================================
            # prompt_key = 'summary.prompt.custom'
            # #FraGon 06012021 Asignacion con assignmentID=1 corresponde a asignacion de piezas y unidades, si esta impresa es buscar caja
            # #print("Validacion:", pickingandpass.isPrinted()) and (pickingandpass.isSplitted())            
            # prompt_values=[]
            # if (pickingandpass.isPrinted()) and (pickingandpass.isSplitted()):
            #     prompt_key += '.search.box'
            #     #FraGon 01092021 Se deja unicamente los ultimos 5 digitos de la asignacion de acuerdo a la etiqueta
            #     prompt_values=[str(self._assignment_lut[0]['idDescription'])[-9:-4]]
            #     prompt_values.append(str(self._assignment_lut[0]['idDescription'])[-4:-2])
            # #FraGon 25022021 Asignacion con assignmentID=1 corresponde a asignacion de piezas y unidades, si no esta impresa es abrir caja
            # elif not(pickingandpass.isPrinted()) and (pickingandpass.isSplitted()):
            #     #FraGon 01092021 Se deja unicamente los ultimos 5 digitos de la asignacion de acuerdo a la etiqueta
            #     prompt_values=[str(self._assignment_lut[0]['idDescription'])[-9:-4]]
            #     prompt_key += '.open.box'
            # #FraGon 25022021 Asignacion con assignmentID=2 corresponde a asignacion de cajas
            # elif (pickingandpass.isBox()):
            #     #FraGon 01092021 Se deja unicamente los ultimos 5 digitos de la asignacion de acuerdo a la etiqueta
            #     prompt_values=[str(self._assignment_lut[0]['idDescription'])[-9:-4]]
            #     prompt_key += '.boxes'
            # #FraGon 25022021 Asignacion con assignmentID=3 corresponde a asignacion de estibas
            # elif (pickingandpass.isPallet()):
            #     #FraGon 01092021 Se deja unicamente los ultimos 5 digitos de la asignacion de acuerdo a la etiqueta
            #     prompt_values=[str(self._assignment_lut[0]['idDescription'])[-7:-2]]
            #     prompt_key += '.pallet'       
            # prompt = itext(prompt_key, *prompt_values)
            # prompt_ready(prompt, True)
            #===================================================================
        else:
            for assignment in self._assignment_lut:
                prompt = ''                   
                #check if override prompt set, that one was given
                if assignment['summaryPromptType'] == 2 and assignment['overridePrompt'] == '':
                    assignment['summaryPromptType'] = 0
                
                #build prompt
                if assignment['summaryPromptType'] == 0: #Default Prompt
                    #print("por aqui pasa el prompt")
                    prompt_key = 'summary.prompt'
                    prompt_values = [assignment['idDescription']]
                    #check if chase
                    if assignment['isChase'] == '1': 
                        prompt_key += '.chase'
                    
                    #check if multiple assignments
                    if len(self._assignment_lut) > 1:
                        prompt_key += '.position'
                        prompt_values.insert(0, assignment['position'])
                    
                    #check if goal time
                    if assignment['goalTime'] != 0:
                        prompt_values.append(assignment['goalTime'])
                        if assignment['goalTime'] == 1:
                            prompt_key += '.goaltime.single'
                        else:
                            prompt_key += '.goaltime.multi'
    
                    prompt = itext(prompt_key, *prompt_values)
    
                elif assignment['summaryPromptType'] == 2: #OverridePrompt
                    prompt = assignment['overridePrompt']
                    
                if prompt != '': #May be blank is summaryPromptType = 1
                    prompt_ready(prompt, True)
                
class_factory.set_override(BeginAssignment, BeginAssignment_Custom)