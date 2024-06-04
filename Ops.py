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
    def openSubWindow(mdi_area, window_class, window_instance, setup_signals=None):
        if window_instance is None or window_instance.isClosed:
            sub_window = QMdiSubWindow()
            window_instance = window_class()
            sub_window.setWidget(window_instance)
            sub_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint) # Frameless window
            mdi_area.addSubWindow(sub_window)
            window_instance.isClosed = False
            sub_window.showMaximized()
            
            if setup_signals:
                setup_signals(window_instance)

        else:
            window_instance.showMaximized()

        return window_instance
    
    @staticmethod
    def msgError(self,title, msg):
        self.msgError= QMessageBox()
        self.msgError.setIcon(QMessageBox.Warning)
        self.msgError.setWindowTitle(title)
        self.msgError.setText(msg)
        self.msgError.show()
    # @staticmethod
    # def clickAndLoad(self):
    #     for button, (window_class, mdi_area_name) in self.button_window_map.items():
    #         if mdi_area_name:
    #             button.clicked.connect(lambda checked, wc=window_class, name=mdi_area_name: Ops.loadSubWindow(self, wc, name))
    #         else:
    #             button.clicked.connect(lambda checked, wc=window_class: Ops.loadWindow(self, wc))

#Load Methods using intances
    # @staticmethod
    # def loadSubWindowInstance(self, window, mdi_area_name):
    #     sub_window = QMdiSubWindow()
    #     sub_window.setWidget(window)
    #     sub_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint) #Frameless window
    #     sub_window.setAttribute(Qt.WA_DeleteOnClose)
    #     mdi_area = self.widgets[mdi_area_name]
    #     mdi_area.addSubWindow(sub_window)
    #     sub_window.show()

    # @staticmethod
    # def loadWindowInstance(self, window):
    #     self.window = window
    #     self.window.show()
    #     self.close()

    # @staticmethod
    # def clickAndLoadInstace(self):
    #     for button, (window_instance, mdi_area_name) in self.button_window_map.items():
    #         if mdi_area_name:
    #             button.clicked.connect(lambda checked, wi=window_instance, name=mdi_area_name: Ops.loadSubWindowInstance(self, wi, name))

    #         else:
    #             button.clicked.connect(lambda checked, wi=window_instance: Ops.loadWindowInstance(self, wi))
    
