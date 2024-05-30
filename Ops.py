from PyQt5.QtWidgets import QMdiSubWindow
from PyQt5 import uic
from PyQt5.QtCore import Qt
from pathlib import Path

DIRECTORY_GUI= "GUI_Windows"

class Ops():
    @staticmethod
    def load_ui(filename, window):
        root_dir = Path(__file__).resolve().parent
        filepath = root_dir / DIRECTORY_GUI / filename
        uic.loadUi(filepath, window)

    @staticmethod
    def loadWidgets(window,widget_setup):
        window.widgets = {}
        if widget_setup:
            for widget_name, widget_type in widget_setup.items():
                window.widgets[widget_name] = window.findChild(widget_type, widget_name)

#load methods using classes  
    @staticmethod
    def loadSubWindow(self, window_class, mdi_area_name):
        window = window_class()
        sub_window = QMdiSubWindow()
        sub_window.setWidget(window)
        sub_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint) #Frameless window
        sub_window.setAttribute(Qt.WA_DeleteOnClose)
        mdi_area = self.widgets[mdi_area_name]
        mdi_area.addSubWindow(sub_window)
        sub_window.showMaximized()

    @staticmethod
    def loadWindow(self, window_class):
        self.window = window_class()
        self.window.show()
        self.close()

    @staticmethod
    def clickAndLoad(self):
        for button, (window_class, mdi_area_name) in self.button_window_map.items():
            if mdi_area_name:
                button.clicked.connect(lambda checked, wc=window_class, name=mdi_area_name: Ops.loadSubWindow(self, wc, name))
            else:
                button.clicked.connect(lambda checked, wc=window_class: Ops.loadWindow(self, wc))

#Load Methods using intances
    @staticmethod
    def loadSubWindowInstance(self, window, mdi_area_name):
        sub_window = QMdiSubWindow()
        sub_window.setWidget(window)
        sub_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint) #Frameless window
        sub_window.setAttribute(Qt.WA_DeleteOnClose)
        mdi_area = self.widgets[mdi_area_name]
        mdi_area.addSubWindow(sub_window)
        sub_window.show()

    @staticmethod
    def loadWindowInstance(self, window):
        self.window = window
        self.window.show()
        self.close()

    @staticmethod
    def clickAndLoadInstace(self):
        for button, (window_instance, mdi_area_name) in self.button_window_map.items():
            if mdi_area_name:
                button.clicked.connect(lambda checked, wi=window_instance, name=mdi_area_name: Ops.loadSubWindowInstance(self, wi, name))

            else:
                button.clicked.connect(lambda checked, wi=window_instance: Ops.loadWindowInstance(self, wi))


    