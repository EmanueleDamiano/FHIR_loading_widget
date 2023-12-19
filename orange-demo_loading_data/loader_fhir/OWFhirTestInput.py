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


class OWFhirTestInput(widget.OWWidget):
    name = "Test input widget"
    description = "test input"
    category = "Development"
    
    class Inputs:
        list_of_paths = widget.Input("Bundle Resource Paths", list)

    def __init__(self):
        super().__init__()

        self.input_received = None 

        # self.set_input(self.Inputs.list_of_paths)


    def create_table(self,json_data):
        pass


    def extract_patient(self, path):
        with open(path,"r") as f:
            bundle_data = json.load(f)
            patient_resource  = bundle_data["entry"][0]["resource"]
            patient_resource  = self.create_table(patient_resource) 
            f.close()
        return patient_resource
    

    @Inputs.list_of_paths
    def set_input(self, value): 
        self.input_value = value
        if self.input_value is not None :
            print("recived this output from prev. widget : ", self.input_value)
            for path in self.input_value:
                patient = self.extract_patient(path)
                print("extracted data for patient: \n",patient )


        

        
# if __name__ == "__main__":
#     widgetpreview.WidgetPreview(OWFhirTestInput).run()


