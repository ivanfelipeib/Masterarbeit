from PyQt5.QtWidgets import QMdiSubWindow, QMessageBox,QFileDialog
from PyQt5 import uic
from PyQt5.QtCore import Qt
from datetime import datetime
import constants
import xlsxwriter

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
    
    def accessDictByPath(nested_dict, path):
        keys = path.split('.')
        value = nested_dict
        try:
            for key in keys:
                value = value[key]
            return value
        except KeyError:
            return None

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

    def generateExcelReport(self, filepath:str, data:dict):
        current_date = datetime.now().strftime('%d-%m-%Y')
        # Create a workbook and add a worksheet
        workbook = xlsxwriter.Workbook(filepath)
        worksheet = workbook.add_worksheet()
        #Add Styles
        header = workbook.add_format({'bold': True, 'font_size': 15, 'underline': 2})
        titles = workbook.add_format({'bold': True, 'font_size': 13, 'underline': 1})
        bold = workbook.add_format({'bold': True})
        underlined = workbook.add_format({'underline': 1})
        #Add fix titles
        worksheet.write(0, 0, "IFC Information Report", header)
        worksheet.write(1, 0, "IFC File", bold)
        worksheet.write(2, 0, "Date of report", bold)

        worksheet.write(4, 0, "Basic Information", titles)
        worksheet.write(5, 0, "IFC Schema",bold)
        worksheet.write(6, 0, "Project Base Point", bold)
        worksheet.write(7, 0, "Coordinate System", bold)
        worksheet.write(8, 0, "Ref.Latitude", bold)
        worksheet.write(9, 0, "Ref.Longitude", bold)
        worksheet.write(10, 0, "Authoring Software", bold)
        worksheet.write(11, 0, "Objects in Model", bold)

        worksheet.write(4, 2, "Project Information", titles)
        worksheet.write(5, 2, "Description", bold)
        worksheet.write(6, 2, "Phase", bold)
        worksheet.write(7, 2, "Organization", bold)
        worksheet.write(8, 2, "Author", bold)

        worksheet.write(13, 0, "Contents of selected IFC Element", titles)
        worksheet.write(14, 0, "Entity", bold)
        worksheet.write(15, 0, "Element", bold)
        worksheet.write(17, 0, "Attributes", titles)
        worksheet.write(17, 2, "Property Sets", titles)
        # Write values
        worksheet.write(1, 1, data["ifc_info"]["File"])
        worksheet.write(2, 1, current_date)
        worksheet.write(5, 1, data["basic_info"]["ifc_schema"])
        worksheet.write(6, 1, data["basic_info"]["base_point"])
        worksheet.write(7, 1, data["basic_info"]["coord_system"])
        worksheet.write(8, 1, data["basic_info"]["latitude"])
        worksheet.write(9, 1, data["basic_info"]["longitude"])
        worksheet.write(10, 1, data["basic_info"]["software"])
        worksheet.write(11, 1, data["basic_info"]["objects_num"])
        worksheet.write(5, 3,data["project_info"]["description"])
        worksheet.write(6, 3,data["project_info"]["phase"])
        worksheet.write(7, 3,data["project_info"]["organization"])
        worksheet.write(8, 3,data["project_info"]["author"])
        worksheet.write(14, 1, data["ifc_info"]["Entity"])
        worksheet.write(15, 1, data["ifc_info"]["Element"])
        
        # Write Attribute
        if "Attributes" in data["ifc_info"]:
            row_start=18
            col_start =0
            attributes=data["ifc_info"]["Attributes"]
            for idx, attr in enumerate(attributes):
                worksheet.write(row_start + idx, col_start, attr)
        # Write PSets
        if "PSets" in data["ifc_info"]:
            psets = data["ifc_info"]["PSets"]
            row_start = 18
            col_start=2
            for key in psets.keys():
                worksheet.write(row_start, col_start, key, bold)
                properties= psets[key]
                for idx, attr in enumerate(properties):
                    worksheet.write(row_start+ 1 + idx, col_start, attr)
                col_start+=1
            last_column=col_start
        else:
            last_column=3 #assuming there is no Property sets in model
        #Adjust column width
        worksheet.set_column(0, last_column,30)
        # Close the workbook
        workbook.close()
        Ops.msgError(self, "Report created", f"Excel file has been created successfully in {filepath}.")
    
    def formatLatLong(coordinates:tuple)->str:
        degrees = coordinates[0]
        minutes = coordinates[1]
        seconds = coordinates[2]

        # Formatting the string
        formatted_string = f"{degrees}° {minutes}' {seconds}''"

        # Display the result
        return(formatted_string)

    @staticmethod
    def msgError(self,title, msg):
        self.msgError= QMessageBox()
        self.msgError.setIcon(QMessageBox.Warning)
        self.msgError.setWindowTitle(title)
        self.msgError.setText(msg)
        self.msgError.show()
