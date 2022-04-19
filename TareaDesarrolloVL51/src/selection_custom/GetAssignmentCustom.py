'''
Created on 8/03/2021

@author: FranciscoGonzalez
'''
from vocollect_core.utilities import class_factory
from vocollect_core import itext
from vocollect_core.dialog.functions import prompt_yes_no, prompt_ready
from selection.GetAssignment import GetAssignmentBase, GetAssignmentAuto
from selection_custom.PickingAndPassCustom import PickingAndPass as PAP
from common.VoiceLinkLut import VoiceLinkLut
from selection_custom.CheckBoxUOM import CheckBoxUOM

class GetAssignmentAuto_Custom(GetAssignmentAuto):
    #----------------------------------------------------------
    def xmit_assignments(self):
        ''' transmit assignment request '''
        GetAssignmentBase.xmit_assignments(self)

        if not self._inprogress_work and self.next_state is None:
            max_ids = self._region_config_rec['maxNumberWordID']
            assignments = self._assignment_lut.number_of_assignments()
            if max_ids > 1 and assignments < self._number_work_ids:
                if assignments == 1:
                    prompt_ready(itext('selection.only.available.single', assignments))
                else:
                    prompt_ready(itext('selection.only.available.plural', assignments))
    
    #----------------------------------------------------------
    def prompt_reverse(self):
        # 27032021 Sobreescribo metodo para que haga esto en vez del original de la tarea
        #FraGon 06012021 Utilizo lut de impresion para generar dialogo adicional de caja nueva o caja media
        # y cambiar prompt de bienvenida, se dice antes del picking inverso
        pickingandpass=PAP()
        self._picks_lut._picking_order = 0
        lut = VoiceLinkLut('prTaskLUTCustomCheckForPrint')
        lut.do_transmit(self._assignment_lut[0]['assignmentID'])
        #02112021 FraGon Se comenta isLastLut por unificacion de LUTs desarrolladas
        #islast_lut= VoiceLinkLut('prTaskLUTCustomCheckForLast')
        #islast_lut.do_transmit(self._assignment_lut[0]['assignmentID'])
        PAP(lut)
        CheckBoxUOM().resetBoxUOM()
        CheckBoxUOM(self._assignment_lut)
        #FraGon 06012021 Pregunta si asignacion es de tipo split
        if pickingandpass.isAsgDev():
            prompt_key = 'summary.prompt.custom'
            #FraGon 06012021 Asignacion con assignmentID=1 corresponde a asignacion de piezas y unidades, si esta impresa es buscar caja
            #print("Validacion:", pickingandpass.isPrinted()) and (pickingandpass.isSplitted())
            #FraGon 30032022 Se agrega logica de caja plastica para control de dialogos con el valor customernumber de asignacion en todos los casos
            prompt_values=[]
            if (pickingandpass.isPrinted()) and (pickingandpass.isSplitted()):
                #FraGon 01092021 Se deja unicamente los ultimos 5 digitos de la asignacion de acuerdo a la etiqueta
                if CheckBoxUOM().isBoxUOM():
                    prompt_key += '.search.box.uom'                
                    prompt_values=[str(self._assignment_lut[0]['idDescription'])[-9:-4]]
                    prompt_values.append(str(CheckBoxUOM().getvalueKindOfBox()))
                    prompt_values.append(str(self._assignment_lut[0]['idDescription'])[-4:-2])                
                else:
                    prompt_key += '.search.box'                
                    prompt_values=[str(self._assignment_lut[0]['idDescription'])[-9:-4]]
                    prompt_values.append(str(self._assignment_lut[0]['idDescription'])[-4:-2])
            #FraGon 25022021 Asignacion con assignmentID=1 corresponde a asignacion de piezas y unidades, si no esta impresa es abrir caja
            elif not(pickingandpass.isPrinted()) and (pickingandpass.isSplitted()):
                #FraGon 01092021 Se deja unicamente los ultimos 5 digitos de la asignacion de acuerdo a la etiqueta
                if CheckBoxUOM().isBoxUOM():
                    prompt_values=[str(CheckBoxUOM().getvalueKindOfBox())]
                    prompt_key += '.open.box.uom'
                else:
                    prompt_values=[str(self._assignment_lut[0]['idDescription'])[-9:-4]]
                    prompt_key += '.open.box'
            #FraGon 25022021 Asignacion con assignmentID=2 corresponde a asignacion de cajas
            elif (pickingandpass.isBox()):
                #FraGon 01092021 Se deja unicamente los ultimos 5 digitos de la asignacion de acuerdo a la etiqueta
                if CheckBoxUOM().isBoxUOM():
                    prompt_values=[str(self._assignment_lut[0]['idDescription'])[-9:-4]]
                    prompt_values.append(str(CheckBoxUOM().getvalueKindOfBox()))
                    prompt_key += '.boxes.uom'
                else:
                    prompt_values=[str(self._assignment_lut[0]['idDescription'])[-9:-4]]
                    prompt_key += '.boxes'
            #FraGon 25022021 Asignacion con assignmentID=3 corresponde a asignacion de estibas
            elif (pickingandpass.isPallet()):
                #FraGon 01092021 Se deja unicamente los ultimos 5 digitos de la asignacion de acuerdo a la etiqueta
                prompt_values=[str(self._assignment_lut[0]['idDescription'])[-7:-2]]
                prompt_key += '.pallet'       
            prompt = itext(prompt_key, *prompt_values)
            prompt_ready(prompt, True)
        if self._region_config_rec['allowReversePicking'] == '1':
            if prompt_yes_no(itext('selection.pick.reverse.order.custom'), True):
                self._picks_lut._picking_order = 1
                #27032021 FraGon se salta para generar rapidez en el dialogo
                #prompt_only(itext('selection.get.reverse.order'))
    
class_factory.set_override(GetAssignmentAuto, GetAssignmentAuto_Custom)