'''
Created on 13/01/2021

@author: FranciscoGonzalez
'''
from vocollect_core.utilities import class_factory, obj_factory
from selection.SelectionVocabulary import SelectionVocabulary
from vocollect_core.task.dynamic_vocabulary import Vocabulary
from selection.SharedConstants import PICK_PROMPT_TASK_NAME
from selection import PickPrompt
from vocollect_core.utilities.localization import itext
from vocollect_core.dialog.functions import prompt_only, prompt_ready
from common.VoiceLinkLut import VoiceLinkLut
from selection_custom.PickingAndPassCustom import PickingAndPass as PAP
from selection_custom.CheckBoxUOM import CheckBoxUOM
from voice import get_voice_application_property
from selection.SelectionLuts import RegionConfig

class SelectionVocabulary_Custom(SelectionVocabulary):
    
        def __init__(self, runner):
            self.vocabs = {'UPC':              obj_factory.get(Vocabulary,'UPC', self._upc, False),
                       'how much more':    obj_factory.get(Vocabulary,'how much more', self._how_much_more, False),
                       'store number':     obj_factory.get(Vocabulary,'store number', self._store_number, False),
                       'route number':     obj_factory.get(Vocabulary,'route number', self._route_number, False),
                       'item number':      obj_factory.get(Vocabulary,'item number', self._item_number, False),
                       'description':      obj_factory.get(Vocabulary,'description', self._description, False),
                       'location':         obj_factory.get(Vocabulary,'location', self._location, False),
                       'quantity':         obj_factory.get(Vocabulary,'quantity', self._quantity, False),
                       'repeat last pick': obj_factory.get(Vocabulary,'repeat_last_pick', self._repeat_last_pick, False),
                       'repick skips':     obj_factory.get(Vocabulary,'repick skips', self._repick_skips, False),
                       'new container':    obj_factory.get(Vocabulary,'new container', self._new_container, False),
                       'close container':  obj_factory.get(Vocabulary,'close container', self._close_container, False),
                       'reprint labels':   obj_factory.get(Vocabulary,'reprint_labels', self._reprint_labels, False),
                       'review contents':  obj_factory.get(Vocabulary,'review_contents', self._review_contents, False),
                       'review cluster':   obj_factory.get(Vocabulary,'review_cluster', self._review_cluster, False),
                       'pass assignment':  obj_factory.get(Vocabulary,'pass assignment', self._pass_assignment, False),
                       'assignment number': obj_factory.get(Vocabulary,'assignment number', self._assignment_number, False),
                       'figure': obj_factory.get(Vocabulary,'figure', self._active_figure, False)
                       }
            self.runner = runner
    
            #previous pick information
            self.previous_picks = []
            self.pick_tasks = []
            self.clear()
    
            self._pass_inprogress = False
            
        def _valid(self, vocab):
            ''' Determines if a vocabulary word is currently valid
            
            Parameters:
                    vocab - vocabulary word to check
                    
            returns - True if word is valid as this time, otherwise false
            '''
            current_task = self.runner.get_current_task().name
            
            #available while picking
            if vocab == 'store number':
                return len(self.current_picks) > 0
            
            elif vocab == 'route number':
                return len(self.current_picks) > 0
    
            elif vocab == 'how much more':
                return len(self.current_picks) > 0
    
            elif vocab == 'repeat last pick':
                return len(self.current_picks) > 0 or len(self.previous_picks) 
            
            elif vocab == 'new container':
                return len(self.current_picks) > 0
                                    
            elif vocab == 'close container':
                #operator not allowed to close container after entering a quantity
                after_qty_prompt = False
                pick_prompt = self.runner.findTask(PICK_PROMPT_TASK_NAME)
                if pick_prompt is not None:
                    after_qty_prompt = (pick_prompt.current_state not in [PickPrompt.SLOT_VERIFICATION,
                                                                         PickPrompt.CASE_LABEL_CD,
                                                                         PickPrompt.ENTER_QTY,
                                                                         PickPrompt.QUANTITY_VERIFICATION])
    
                return (len(self.current_picks) > 0 
                        and self.region_config_rec['containerType'] != 0
                        and not after_qty_prompt)
            
            elif vocab == 'reprint labels':
                return len(self.current_picks) > 0
                   
            elif vocab == 'repick skips':
                return len(self.current_picks) > 0 
            
            elif vocab == 'review cluster':
                return len(self.current_picks) > 0 
    
            elif vocab == 'review contents':
                return len(self.current_picks) > 0 
                                
            elif vocab == 'UPC':
                return (len(self.current_picks) > 0 
                        and current_task in self.pick_tasks)
            
            elif vocab == 'item number':
                return (len(self.current_picks) > 0 
                        and current_task in self.pick_tasks)
    
            elif vocab == 'description':
                return (len(self.current_picks) > 0 
                        and current_task in self.pick_tasks)
    
            elif vocab == 'location':
                return (len(self.current_picks) > 0 
                        and current_task in self.pick_tasks)
            
            elif vocab == 'quantity':
                return (len(self.current_picks) > 0 
                        and current_task in self.pick_tasks)
            
            elif vocab == 'pass assignment':
                return len(self.current_picks) > 0 
            
            elif vocab == 'assignment number':
                return len(self.current_picks) > 0
    
            return False
        
        def _new_container(self):
            ''' launch new container task'''
            put_prompt = False
            pick_task = self.runner.findTask(PICK_PROMPT_TASK_NAME)
            if pick_task is not None:
                put_prompt = pick_task.current_state == PickPrompt.PUT_PROMPT
            #print("Imprimo assignment_lut",  self.assignment_lut)
            pickingandpass=PAP()
            if (pickingandpass.isLUTEmpty()):
                lut = VoiceLinkLut('prTaskLUTCustomCheckForPrint')
                #02112021 FraGon Se comenta isLastLut por unificacion de LUTs desarrolladas
                #islast_lut = VoiceLinkLut('prTaskLUTCustomCheckForLast')
                pickingandpass=PAP(lut.do_transmit(self.assignment_lut[0]['assignmentID']))
            #FraGon 06012021 Pregunta si asignacion es de tipo split
            if pickingandpass.isAsgDev():
                if pickingandpass.isBox():
                    prompt_only(itext('selection.new.container.not.allowed'))
                elif pickingandpass.isPallet():
                    prompt_only(itext('selection.new.container.not.allowed'))
                elif self.region_config_rec['containerType'] == 0:
                    prompt_only(itext('selection.new.container.not.allowed'))
                elif len(self.assignment_lut) == 1:
                    self._launch_new_container(self.assignment_lut[0])
                elif put_prompt:
                    self._launch_new_container(pick_task._curr_assignment)
                else:
                    prompt_only(itext('selection.new.container.multiple.put.prompt'))
                pass
            else:
                #FraGon 21042022 Confirma al operador que no es posible abrir contenedor
                prompt_only(itext('selection.new.container.not.allowed'))
            #===================================================================
            # #===================================================================
            # # SE COMENTA PARA NO USAR NUEVO CONTENEDOR USANDO TAREA PICKING POR ZONAS EN REGIONES PICKING ESTANDAR
            # #===================================================================
            # 
            # else:
            #     if self.region_config_rec['containerType'] == 0:
            #         prompt_only(itext('selection.new.container.not.allowed'))
            #     elif len(self.assignment_lut) == 1:
            #         self._launch_new_container(self.assignment_lut[0])
            #     elif put_prompt:
            #         self._launch_new_container(pick_task._curr_assignment)
            #     else:
            #         prompt_only(itext('selection.new.container.multiple.put.prompt'))
            #===================================================================
                
            return True
        
        
        def _assignment_number(self):
            #FraGon 06012021 Utilizo lut de impresion para generar dialogo adicional de caja nueva o caja media
            # y cambiar prompt de bienvenidaz
            #print("Imprimo assignment_lut", self.assignment_lut)
            pickingandpass=PAP()
            if (pickingandpass.isLUTEmpty()):
                lut = VoiceLinkLut('prTaskLUTCustomCheckForPrint')
                islast_lut = VoiceLinkLut('prTaskLUTCustomCheckForLast')
                pickingandpass=PAP(lut.do_transmit(self.assignment_lut[0]['assignmentID']),
                                   islast_lut.do_transmit(self.assignment_lut[0]['assignmentID']))
            if pickingandpass.isAsgDev():
                prompt_key = 'summary.prompt.custom'
                #FraGon 06012021 Asignacion con assignmentID=1 corresponde a asignacion de piezas y unidades, si esta impresa es buscar caja
                #print("Validacion:", pickingandpass.isPrinted()) and (pickingandpass.isSplitted())
                prompt_values=[]
                #print("Validacion mensaje:",CheckBoxUOM().isBoxUOM())
                if (pickingandpass.isPrinted()) and (pickingandpass.isSplitted()):
                    #FraGon 01092021 Se deja unicamente los ultimos 5 digitos de la asignacion de acuerdo a la etiqueta
                    if CheckBoxUOM().isBoxUOM():
                        prompt_key += '.search.box.uom'                
                        prompt_values=[str(self.assignment_lut[0]['idDescription'])[-9:-4]]
                        prompt_values.append(str(CheckBoxUOM().getvalueKindOfBox()))
                        prompt_values.append(str(self.assignment_lut[0]['idDescription'])[-4:-2])
                    else:
                        prompt_key += '.search.box'
                        #FraGon 01092021 Se deja unicamente los ultimos 5 digitos de la asignacion de acuerdo a la etiqueta
                        prompt_values=[str(self.assignment_lut[0]['idDescription'])[-9:-4]]
                        prompt_values.append(str(self.assignment_lut[0]['idDescription'])[-4:-2])
                #FraGon 25022021 Asignacion con assignmentID=1 corresponde a asignacion de piezas y unidades, si no esta impresa es abrir caja
                elif not(pickingandpass.isPrinted()) and (pickingandpass.isSplitted()):
                    #FraGon 01092021 Se deja unicamente los ultimos 5 digitos de la asignacion de acuerdo a la etiqueta
                    if CheckBoxUOM().isBoxUOM():
                        prompt_values=[str(CheckBoxUOM().getvalueKindOfBox())]
                        prompt_key += '.open.box.uom'
                    else:
                        #FraGon 01092021 Se deja unicamente los ultimos 5 digitos de la asignacion de acuerdo a la etiqueta
                        prompt_values=[str(self.assignment_lut[0]['idDescription'])[-9:-4]]
                        prompt_key += '.open.box'
                #FraGon 25022021 Asignacion con assignmentID=2 corresponde a asignacion de cajas
                elif (pickingandpass.isBox()):
                    #FraGon 01092021 Se deja unicamente los ultimos 5 digitos de la asignacion de acuerdo a la etiqueta
                    if CheckBoxUOM().isBoxUOM():
                        prompt_values=[str(self.assignment_lut[0]['idDescription'])[-9:-4]]
                        prompt_values.append(str(CheckBoxUOM().getvalueKindOfBox()))
                        prompt_key += '.boxes.uom'
                    else:
                        #FraGon 01092021 Se deja unicamente los ultimos 5 digitos de la asignacion de acuerdo a la etiqueta
                        prompt_values=[str(self.assignment_lut[0]['idDescription'])[-9:-4]]
                        prompt_key += '.boxes'
                #FraGon 25022021 Asignacion con assignmentID=3 corresponde a asignacion de estibas
                elif (pickingandpass.isPallet()):
                    #FraGon 01092021 Se deja unicamente los ultimos 5 digitos de la asignacion de acuerdo a la etiqueta
                    prompt_values=[str(self.assignment_lut[0]['idDescription'])[-7:-2]]
                    prompt_key += '.pallet'       
                prompt = itext(prompt_key, *prompt_values)
                prompt_ready(prompt, True)
            return True
        
        def _active_figure(self):
            #FraGon 30082022 Utilizo lut para obtener figura activa
            lut = VoiceLinkLut('prTaskLUTActiveFigure') ## EL NOMBRE DE LA LUT CAMBIA --MODIFICACIÓN--
            activeFigure = lut.do_transmit(self.assignment_lut[0]['assignmentID']) ##ESTE PARAMETRO PUEDE CAMBIA O INCLUSO ESTAR VACIO
            [print("Imprimo lo que contiene activeFigure", activeFigure)] ##ESTO SE PUEDE COMENTAR DESPUES DE PROBAR LA LUT
            prompt = itext('selection.prompt.active.figure', activeFigure[0]['figure']) ##AQUI SE CONTRUYE EL ANUNCIO PARA EL OPERADOR
            prompt_ready(prompt, True)
            return True

class_factory.set_override(SelectionVocabulary, SelectionVocabulary_Custom)