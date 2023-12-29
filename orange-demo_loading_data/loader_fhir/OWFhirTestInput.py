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
import re 
import requests


class OWFhirTestInput(widget.OWWidget):
    name = "Test input widget"
    description = "test input"
    category = "Development"
    
    class Inputs:
        list_of_paths = widget.Input("Bundle Resource Paths", list)

    class Outputs:
        processed_table = widget.Output("Processed Patient Table", Table)


    def __init__(self):
        super().__init__()


        self.result_dict = {} ## dict for extracting all the nested info. in the resource
        self.data_values = [] ## rows to append in the final table
        self.input_received = None 
        box = gui.widgetBox(self.controlArea,"")
        box.setFixedHeight(100)
        # self.set_input(self.Inputs.list_of_paths)
        ## campo per immettere stringa dell APi da cui fare richiesta
        self.test_input = "" ## inital default value for input
        self.input_line = gui.lineEdit(widget=box, master=self,value="test_input", label="Input a fhir server endpoit to retrieve data for a patient ",validator=None,callback=self.validate_api)
        gui.button(box, master = self, label = "send", callback=self.validate_api)

        gui.separator(self)
        box2  = gui.widgetBox(self.controlArea,"")
        self.display_message = gui.widgetLabel(box2," ")        



    def validate_api(self):
        ## se input è una stringa valida che corrisponde alla forma di un endpoint, si passa alla funzione che fa la request
        api_pattern = r'^https?://(?:\w+\.)?\w+\.\w+(?:/\S*)?$'
        if re.match(api_pattern, self.test_input):
            self.make_request()
        else:
            print("input a valid fhir api")
            self.display_message.setText("ERROR: Input a valid FHIR API")


    def make_request(self):
        try:
            response = requests.get(self.test_input)
        except:
            print("error while making request")
            self.display_message.setText("error while making request")
            return
        # response = requests.get("https://spark.incendi.no/fhir/Patient/3")
        json_results = response.json()
        self.process_item(json_results)
        print("results of processing: ", self.result_dict)
        self.create_table()
        # print("obtained this json", json_results)



    def process_item(self, x = dict(),prefix = ""):
        for field in x.items():
            if prefix != "":
                key = prefix + field[0]
            else:
                key = field[0]
            value = field[1]
            if isinstance(value, list):
                if len(value) == 1:
                    if isinstance(value[0], str):
                        self.result_dict[key] = value[0]
                        continue
                    self.process_item(value[0],prefix=f"{key}_")
                    continue
                else:	
                    continue
            if isinstance(value,dict):
                self.process_item(value,prefix=f"{key}_")
                continue
                # print(f"key {field[0]} \n and value {field[1]}")
            self.result_dict[key] = value



    def create_table(self):
        # print("inserted: ", self.test_input)
        string_features = []
        cont_features   = []
        for field in self.result_dict.items():
            column = field[0]
            value = field[1]
            if isinstance(value,str):
                string_features.append(StringVariable(column)) 
            else:
                try:
                    cont_features.append(ContinuousVariable(column))
                except:
                    print(column, value, "gave error")

        self.data_values.append([values for values in self.result_dict.values()])
        # datatable = Orange.data.Table(features,data_values)
        # domain = Domain(cont_features,metas = string_features)
        domain = Domain([],metas = string_features)
        output_table = Table(domain,
                                    
                                        self.data_values
                                    )
        print("create table: \n", output_table)
        self.Outputs.processed_table.send(output_table)

    def extract_patient(self, path):
        with open(path,"r") as f:
            bundle_data = json.load(f)
            patient_resource  = bundle_data["entry"][0]["resource"]
            self.process_item(patient_resource) 
            f.close()
    
        self.create_table()
    

    @Inputs.list_of_paths
    def set_input(self, value): 
        self.input_value = value
        if self.input_value is not None :
            print("recived this output from prev. widget : ", self.input_value)
            for path in self.input_value:
                self.extract_patient(path)
                print("extracted data for patient: \n",self.result_dict )
        print("final length of the dict: ", len(self.result_dict))
        print("final result dict: \n", self.result_dict)

        

        
# if __name__ == "__main__":
#     widgetpreview.WidgetPreview(OWFhirTestInput).run()


