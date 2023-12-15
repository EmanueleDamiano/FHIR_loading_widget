import sys
import numpy

import Orange.data
from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.signals import Input, Output


class OWDataSamplerA(widget.OWWidget):
    name = "Import FHIR Patient"
    description = "Randomly selects a subset of instances from the data set"
    
    priority = 10

    # priority defines the order in which the widget appears in the widget toolbox or menu when users access or search for widgets within the Orange data mining software.

    class Inputs:
        # data = Input()
        data = Input("Data", Orange.data.Table)

    class Outputs:
        sample = Output("Sampled Data", Orange.data.Table)

    sample_size = settings.Setting(50)
    commit_on_change = settings.Setting(0)
    ## use with gui, to be defined in init

    want_main_area = False

    def __init__(self):
        super().__init__()

        # GUI
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(
            box, "No data on input yet, waiting to get something.")
        self.infob = gui.widgetLabel(box, '')
        
        gui.separator(self.controlArea)
        ## defining here input for setting the sample size
        self.optionsBox = gui.widgetBox(self.controlArea, "Options")
        gui.spin(
            self.optionsBox,
            self,
            "sample_size", ## any change in the spin box control will automatically be propagated to self."" and vice-versa defining it in the code
            minv=10,
            maxv=90,
            step=10,
            label="Sample Size [%]:",
            callback=[self.selection, self.checkCommit],
        )
        gui.checkBox(
            self.optionsBox, self, "commit_on_change", "Commit data on selection change"
        )
        gui.button(self.optionsBox, self, "Commit", callback=self.commit)
        self.optionsBox.setDisabled(True)

    @Inputs.data
    def set_data(self, dataset):
        ## set data => selection (ottiene sample) => commit (invia a classe output)
        if dataset is not None:
            self.dataset = dataset
            self.infoa.setText("%d instances in input dataset" % len(dataset))
            self.optionsBox.setDisabled(False)
            self.selection()
        else:
            self.dataset = None
            self.sample = None
            self.optionsBox.setDisabled(False)
            self.infoa.setText("No data on input yet, waiting to get something.")
            self.infob.setText("")
        self.commit()

    def selection(self):
        if self.dataset is None:
            return

        n_selected = int(numpy.ceil(len(self.dataset) * self.sample_size / 100.0))
        indices = numpy.random.permutation(len(self.dataset))
        indices = indices[:n_selected]
        self.sample = self.dataset[indices]
        self.infob.setText("%d sampled instances" % len(self.sample))

    def commit(self):
        self.Outputs.sample.send(self.sample)

    def checkCommit(self):
        if self.commit_on_change:
            self.commit()

            