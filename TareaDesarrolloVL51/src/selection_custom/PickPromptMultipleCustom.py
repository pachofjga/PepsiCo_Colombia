'''
Created on 27/03/2021

@author: FranciscoGonzalez
'''
from vocollect_core.utilities import class_factory
from selection.PickPromptMultiple import PickPromptMultipleTask
from vocollect_core.utilities.localization import itext
from vocollect_core.dialog.functions import prompt_digits, prompt_ready
from selection.SharedConstants import ENTER_QTY
from selection_custom.CheckBoxUOM import CheckBoxUOM


class PickPromptMultipleTask_Custom(PickPromptMultipleTask):
    
    #----------------------------------------------------------
    def enter_qty(self):
        ''' Enter quantity'''

        additional_vocabulary = {'skip slot' : False, 'partial' : False}
            
        #prompt user for quantity
        if self._region["qtyVerification"] == "1" or self._short_product or self._partial:
            if self._short_product:
                prompt = itext('selection.pick.prompt.short.product.quantity')
            elif self._partial:
                prompt = itext('selection.pick.prompt.partial.quantity')
                additional_vocabulary['short product'] = False #Add short product to vocab
            else:
                #FraGon 25052021 Se modifica texto de selecciona x producto en unidad de medida y
                #FraGon 30032022 UOM without semicolon in the description
                uom = self._uom.lower()[0:-1]
                if CheckBoxUOM().isBoxUOM():
                    if (uom == "cajas"):
                        prompt = itext("selection.pick.prompt.pick.quantity.custom.uom.boxes",
                                       self._expected_quantity, uom,  CheckBoxUOM().getvalueKindOfBox())
                    else:
                        prompt = itext("selection.pick.prompt.pick.quantity.custom",
                                   self._expected_quantity, self._uom, self._id_description, self._description, self._message,)
                else:
                    prompt = itext("selection.pick.prompt.pick.quantity.custom",
                                   self._expected_quantity, self._uom, self._id_description, self._description, self._message,)
                                
            result = prompt_digits(prompt,
                                   itext("selection.pick.prompt.pick.quantity.help"),
                                   1, len(str(self._expected_quantity)), 
                                   False, False,
                                   additional_vocabulary, hints=[str(self._expected_quantity)])
        else:
            additional_vocabulary['short product'] = False #Add short product to vocab
            #If the quantity verification is not set ask for quantity and take what ever they say
            result = prompt_ready(itext("selection.pick.prompt.pick.quantity", 
                                             self._expected_quantity, self._uom,  self._id_description, self._description, self._message), 
                                  False, 
                                  additional_vocabulary)

        #check results
        if result == 'short product':
            self.next_state = ENTER_QTY
            self._short_product = True
            self._partial = False
        elif result == 'partial':
            self.next_state = ENTER_QTY
            self._validate_partial(self._expected_quantity)
        elif result == 'ready':
            self._picked_quantity = self._expected_quantity
        elif result == 'skip slot':
            self.next_state = ENTER_QTY
            self._skip_slot()
        else:
            self._picked_quantity = int(result)
            if self._picked_quantity == self._expected_quantity:
                self._short_product = False
                self._partial = False
    
    pass

class_factory.set_override(PickPromptMultipleTask, PickPromptMultipleTask_Custom)