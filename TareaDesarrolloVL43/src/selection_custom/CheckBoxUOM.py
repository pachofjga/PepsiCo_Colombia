'''
Created on 30/03/2022

@author: FranciscoGonzalez
'''



class CheckBoxUOM():
    '''VARIABLE CLASSES TO RE USE THE INSTANCE OF ANY OBJECT RELATED WITH CLASS'''
    _flagBoxUOM=None
    _listTypeOfBox=None
    _isPromptActivated=None
    _valueKindOfBoxLower=None
    
    def __init__(self, assignmentLUT=None):
        if assignmentLUT != None:
            # FraGon 30032022 True if summaryPromptType is activated with state = 2
            CheckBoxUOM._isPromptActivated = True if assignmentLUT[0]['summaryPromptType']==2 else False
            #print("Prompt en region esta activado:", CheckBoxUOM._isPromptActivated)
            ## The other positions on the array are the options which customer number is possible
            CheckBoxUOM._listTypeOfBox = assignmentLUT[0]['overridePrompt'].split(",")[0:-1]
            #print("Lista de tipos de caja", CheckBoxUOM._listTypeOfBox)
            ## The latest position in the array is customer number
            CheckBoxUOM._valueKindOfBoxLower = assignmentLUT[0]['overridePrompt'].split(",")[-1].lower()
            #print("Valor a comparar con lista:", CheckBoxUOM._valueKindOfBoxLower)
            ## Check status of variable class
            self._checkCustomerNumber()
            #print("Resultado validacion con lista:", CheckBoxUOM._flagBoxUOM)
        
    def _checkCustomerNumber(self):
        if CheckBoxUOM._flagBoxUOM == None:
            if CheckBoxUOM._isPromptActivated:                            
                for i in range(0,len(self._listTypeOfBox)):
                    if CheckBoxUOM._valueKindOfBoxLower == self._listTypeOfBox[i].lower():
                        CheckBoxUOM._flagBoxUOM=True
                        break
                    elif i==len(self._listTypeOfBox[i].lower())-1:
                        CheckBoxUOM._flagBoxUOM=False
                        break
    
    def isBoxUOM(self):
        return CheckBoxUOM._flagBoxUOM
    
    def resetBoxUOM(self):
        CheckBoxUOM._flagBoxUOM=None
        
    def getvalueKindOfBox(self):
        return CheckBoxUOM._valueKindOfBoxLower
        
        