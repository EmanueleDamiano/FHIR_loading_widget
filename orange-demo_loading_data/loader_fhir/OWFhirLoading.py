import sys
import numpy
import tkinter as tk
from Orange.data import Domain, StringVariable, DiscreteVariable, ContinuousVariable, Table, Values, Tuple
from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.signals import Input, Output
import tkinter as tk
from tkinter import filedialog
import json
from Orange.widgets.utils import widgetpreview


class OWFhirLoading(widget.OWWidget):
    name = "DemoLoading"
    description = "Upload a fhir resource and trasform it to an orange table where you can develop any analytics you need"
    category = "developement"
    class Outputs:
        final_process_table = widget.Output("Processed Data",list)

    def __init__(self):
        super().__init__()

        box = gui.button(self.controlArea, self,label = "Import one or more Json files", callback = self.UploadAction() )
        self.infoa = gui.widgetLabel(
            box, ".")
        self.infob = gui.widgetLabel(box, '')
                
        # root = tk.Tk()
        # button = tk.Button(root, text='Open', command=self.UploadAction)
        # button.pack()
        # root.mainloop()
        # OWFhirConverter.commit()
          

    def select_paths(self,file_path):
        #  print("selected files: ", file_path)
         self.bundle_path = file_path
         print("bundle file path: ",self.bundle_path)
        #  with open(file_path,"r") as file:
        #     res_data = json.load(file)
            
        #     if res_data["resourceType"] != "MedicationRequest":
        #          print("please load a MedicationRequest fhir resource")
        #          return
            
            
        #     final_res = self.convert_Medication_Req(res_data)
        #     print("processed results: ", final_res)
        #     file.close()
        #  self.final_table = self.create_orange_table(final_res)
        #  print("final table: ", self.final_table)
         self.commit()

    def UploadAction(self,event=None):
            file_paths = filedialog.askopenfilenames(
                 title      = "Select json fhir resources",
                #  filetypes  = (("JSON files", ".json"))
            )
            if file_paths:
                 print("file paths list: ", file_paths)
                 self.file_paths = file_paths
                 self.commit()
                #  for file in file_paths:

                #     self.select_paths(file)
                    
            else:
                 print("selected 0 files")
                 return 
            
            
            


    

    
                
    def commit(self):
         self.Outputs.final_process_table.send(self.file_paths)
        

        
if __name__ == "__main__":
    widgetpreview.WidgetPreview(OWFhirLoading).run()