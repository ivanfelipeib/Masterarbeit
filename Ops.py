from PyQt5.QtWidgets import QMdiSubWindow, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import Qt
from pathlib import Path

DIRECTORY_GUI= "GUI_Windows"
DIRECTORY_GUI_FILTERS ="Filters-Requirements"

class Ops():
    @staticmethod
    def load_ui(filename, window, filter= False):
        #UI Elements in filters-requirements folder
        if filter:
            root_dir = Path(__file__).resolve().parent
            filepath = root_dir / DIRECTORY_GUI / DIRECTORY_GUI_FILTERS / filename
            uic.loadUi(filepath, window)
        #UI in GUI_Windows folder
        else:
            root_dir = Path(__file__).resolve().parent
            filepath = root_dir / DIRECTORY_GUI / filename
            uic.loadUi(filepath, window)

    @staticmethod
    def loadWidgets(window,widgets):
        window.widgets = {}
        for name, widget in widgets.items():
            setattr(window, name, window.findChild(widget, name))

    @staticmethod
    def connectHandlers(window, handlers):
        for btn, handler in handlers.items():
            getattr(window, btn).clicked.connect(handler)


    @staticmethod
    def openWindow(window_class, window_instance, setup_signals=None):
        if window_instance is None or window_instance.isClosed:
            window_instance = window_class()
            window_instance.isClosed = False
            window_instance.show()
            if setup_signals:
                setup_signals(window_instance)
        else:
            window_instance.show()
        return window_instance

    @staticmethod
    def openSubWindow(mdi_area, window_class, window_instance, setup_signals=None, my_ids_instance= None, my_spec_instance= None):
        if window_instance is None or window_instance.isClosed: #If window_instance set as None, a new Instance is created
            if my_ids_instance is None:
                sub_window = QMdiSubWindow()
                window_instance = window_class()
                sub_window.setWidget(window_instance)
                sub_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint) # Frameless window
                mdi_area.addSubWindow(sub_window)
                window_instance.isClosed = False
                sub_window.showMaximized()
            
            else:
                sub_window = QMdiSubWindow()
                window_instance = window_class(my_ids_instance, my_spec_instance)
                sub_window.setWidget(window_instance)
                sub_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint) # Frameless window
                mdi_area.addSubWindow(sub_window)
                window_instance.isClosed = False
                sub_window.showMaximized()

            if setup_signals:
                setup_signals(window_instance)

        else: #If window_instance set as an existing instance, existing instance is loaded and no new intance is created. 
            window_instance.showMaximized()

        return window_instance
    
    @staticmethod
    def dateToIsoFormat(date):
        iso_date=date.date().toString(Qt.ISODate)
        return iso_date
    
    @staticmethod
    def dictEmptyValueToNone(dict_data):
        for key, value in dict_data.items():
            if value == "":
                dict_data[key] = None
        return dict_data

    @staticmethod
    def msgError(self,title, msg):
        self.msgError= QMessageBox()
        self.msgError.setIcon(QMessageBox.Warning)
        self.msgError.setWindowTitle(title)
        self.msgError.setText(msg)
        self.msgError.show()
