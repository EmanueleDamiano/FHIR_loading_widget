import sys
import numpy
import tkinter as tk
import Orange.data
from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.signals import Input, Output
import tkinter as tk
from tkinter import filedialog
import json



class OWFhirConverter(widget.OWWidget):
    name = "Fhir resource converter"
    description = "Upload a fhir resource and trasform it to an orange table where you can develop any analytics you need"

    ## ci si concentra su una risorsa specifica per ottenere una tabella più concentrata; composta solo dalle colonne che davvero servono
    

    ## input: una risorsa fhir di un tipo specifico
    # class Inputs: 
        # data = Input("Data", Orange.data.Instance)
    
    class Outputs:
        imported_data = Output("Sampled Data", Orange.data.Instance)

    def __init__(self):
        super().__init__()

        box = gui.Button(self.controlArea, self,label = "Import a Json file", callback = self.UploadAction() )
        self.infoa = gui.widgetLabel(
            box, "No data on input yet, waiting to get something.")
        self.infob = gui.widgetLabel(box, '')
                
        root = tk.Tk()
        button = tk.Button(root, text='Open', command=self.UploadAction)
        button.pack()
        root.mainloop()
        OWFhirConverter.commit()
        
    def UploadAction(self,event=None):
            filename = filedialog.askopenfilename()
            print('reading:', filename)
            with open(filename,"r") as file:
                self.data = json.load(file)
                self.commit()
                file.close()
        


    

    # @Inputs.data
    # def UploadAction(self,event=None):
    #         filename = filedialog.askopenfilename()
    #         print('reading:', filename)
    #         with open(filename,"r") as file:
    #             self.data = json.load(file)

    #             self.commit()
    #             file.close()
                
    def commit(self):
         self.Outputs.imported_data.send(self.data)
        

        
