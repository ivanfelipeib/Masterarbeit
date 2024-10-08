from PyQt5.QtWidgets import QMdiSubWindow, QMessageBox,QFileDialog
from PyQt5 import uic
from PyQt5.QtCore import Qt, QDate
from datetime import datetime
import constants
import xlsxwriter
import re

class Ops():
    @staticmethod
    def load_ui(filename, window, filter= False):
        if filter:
            filepath = constants.GUI_FACETS_DIR + "/" + filename #UI Elements in filters-requirements folder
            uic.loadUi(filepath, window)
        
        else:
            filepath = constants.GUI_DIR + "/"+ filename #UI in GUI_Windows folder
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
    def openWindow(window_class, window_instance, setup_signals=None, ifc_file_path:str=None):
        if window_instance is None or window_instance.isClosed:
            if ifc_file_path: #Case IfcCheckerWindow where ifc_file_path is passed
                window_instance = window_class(None, ifc_file_path)
                window_instance.isClosed = False
                window_instance.show()
                if setup_signals:
                    setup_signals(window_instance) 
            else:
                window_instance = window_class()
                window_instance.isClosed = False
                window_instance.show()
                if setup_signals:
                    setup_signals(window_instance)
        else:
            window_instance.show()
        return window_instance

    @staticmethod
    def openSubWindow(mdi_area, window_class, window_instance, setup_signals=None, my_ids_instance= None, my_spec_instance= None, my_facet_instance=None):
        if window_instance is None or window_instance.isClosed: #If window_instance set as None, a new Instance is created
            if my_ids_instance is None and my_spec_instance is None and my_facet_instance is None: #If no IDS/Spec/Facet instance was passed a new one is created
                sub_window = QMdiSubWindow()
                window_instance = window_class()
                sub_window.setWidget(window_instance)
                sub_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint) # Frameless window
                mdi_area.addSubWindow(sub_window)
                window_instance.isClosed = False
                sub_window.showMaximized()
            
            else: # if ids/spec/facet were passed, it is used to load data
                sub_window = QMdiSubWindow()
                window_instance = window_class(None, my_ids_instance, my_spec_instance, my_facet_instance)
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
    def dateToIsoFormat(date)->str:
        iso_date=date.date().toString(Qt.ISODate)
        return iso_date

    @staticmethod
    def stringToDateFormat(date_str:str)-> QDate:
        date = QDate.fromString(date_str, 'yyyy-MM-dd')
        return date
    
    @staticmethod
    def dictEmptyValueToNone(dict_data) ->dict:
        for key, value in dict_data.items():
            if value == "":
                dict_data[key] = None
        return dict_data

    @staticmethod
    def isValidEmail(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' # Basic regex pattern for email validation
        return re.match(pattern, email) is not None

    def setTextComboBox(window, combo_box_name:str= "comboBox", text:str="Text to search"):
        combo_box_widget = getattr(window, combo_box_name, None)

        if combo_box_widget is None:
            Ops.msgError(window,"Error", f"ComboBox '{combo_box_name}' not found")
            return
        
        index = combo_box_widget.findText(text)
        if index == -1:  # Value not found
            Ops.msgError(window, "Error", f"Value: '{text}' was not found within the ComboBox {combo_box_name} available values.")
        else:
            combo_box_widget.setCurrentIndex(index)
            print(f"Value '{text}' set successfully in {combo_box_name}.")

    def deleteItemInList(window, list_widget_name, text):
        list_widget = getattr(window, list_widget_name, None)
        if not list_widget:
            print(f"Error: {list_widget_name} is not a valid attribute of {window}.")
            return False
        
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if item.text() == text:
                list_widget.takeItem(i)
                return True  # Return True if item is found and deleted
    
        return False  # Return False if item with given text is not found
    
    def isRegex(pattern:str)->bool:
        #Since any string is a valid regex pattern that matches the literal string
        #This method distinguishes between a literal string and a string that is intended to be a regular expression
        #Exclude as well floating-point numbers with decimal indicated by comma or point, since those are proofed as single values not as patterns
        if pattern=="" or pattern is None:
            return False
        
        regex_special_chars = r".^$*+?{}[]\|()"
        contains_special_char = any(char in pattern for char in regex_special_chars)
        
        float_regex = r"^\d+([.,]\d+)?$"  # Define a regex to match floating-point
        if contains_special_char and not re.match(float_regex, pattern):
            return True
        return False
        
    @staticmethod
    def formatDictionary(dictionary, level=0):
        formatted_text = ""
        for key, value in dictionary.items():
            if isinstance(value, dict):
                formatted_text += f"{' ' * (level * 4)}{key}:\n"
                formatted_text += Ops.formatDictionary(value, level + 1)
            else:
                formatted_text += f"{' ' * (level * 4)}{key}: {value}\n"
        return formatted_text
    
    def filePathExport(self):
        options = QFileDialog.Options()
        filter = "Excel files (*.xlsx)"
        destination_file, _ = QFileDialog.getSaveFileName(self, "Select destination filepath", "", filter, options=options)
        return destination_file

    @staticmethod
    def formatLatLong(coordinates)->str:
        if isinstance(coordinates, tuple) and len(coordinates) == 3:
            degrees = coordinates[0]
            minutes = coordinates[1]
            seconds = coordinates[2]

            # Formatting the string
            formatted_string = f"{degrees}° {minutes}' {seconds}''"

            # Display the result
            return(formatted_string)
        else:
            return str(coordinates)
    
    
    @staticmethod
    def getDatetime()->str:
        now = datetime.now()
        formatted_now = now.strftime("%d-%m-%Y %H:%M")
        return formatted_now

    def checkIfElementSelected(window, list_widget):
        if list_widget.count() == 0:
            return False
        elif not list_widget.selectedItems():
            return False
        return True

    @staticmethod
    def msgError(self,title, msg):
        self.msgError= QMessageBox()
        self.msgError.setIcon(QMessageBox.Warning)
        self.msgError.setWindowTitle(title)
        self.msgError.setText(msg)
        self.msgError.show()
