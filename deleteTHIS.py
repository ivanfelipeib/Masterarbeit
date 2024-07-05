import sys
import ifcopenshell
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QLineEdit, QLabel, QFileDialog, QMessageBox

class IfcApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("IFC Importer")

        # Instance variable to store the model
        self.model = None

        # Create the main vertical layout
        main_layout = QVBoxLayout()

        # Create horizontal layout for the import button and add it to the main layout
        button_layout = QHBoxLayout()
        self.import_button = QPushButton("Import_Ifc")
        self.import_button.clicked.connect(self.import_ifc_file)  # Connect the button to the method
        button_layout.addWidget(self.import_button)
        main_layout.addLayout(button_layout)

        # Create horizontal layout for entities combobox and label and add them to the main layout
        entities_layout = QHBoxLayout()
        self.entities_label = QLabel("Entities under IfcProject:")
        entities_layout.addWidget(self.entities_label)
        self.entities_combo = QComboBox()
        entities_layout.addWidget(self.entities_combo)
        main_layout.addLayout(entities_layout)

        # Create horizontal layout for entity instances combobox and label and add them to the main layout
        entity_instances_layout = QHBoxLayout()
        self.entity_instances_label = QLabel("Entity Instances:")
        entity_instances_layout.addWidget(self.entity_instances_label)
        self.entity_instances_combo = QComboBox()
        entity_instances_layout.addWidget(self.entity_instances_combo)
        main_layout.addLayout(entity_instances_layout)

        # Create horizontal layout for attributes combobox and label and add them to the main layout
        attributes_layout = QHBoxLayout()
        attributes_label = QLabel("Attributes:")
        self.attributes_combo = QComboBox()
        attributes_layout.addWidget(attributes_label)
        attributes_layout.addWidget(self.attributes_combo)
        main_layout.addLayout(attributes_layout)

        # Create horizontal layout for line edit and label and add them to the main layout
        line_edit_layout = QHBoxLayout()
        line_edit_label = QLabel("Value:")
        self.line_edit = QLineEdit()
        line_edit_layout.addWidget(line_edit_label)
        line_edit_layout.addWidget(self.line_edit)
        main_layout.addLayout(line_edit_layout)

        # Set the main layout to the main window
        self.setLayout(main_layout)

    def import_ifc_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Import IFC File", "", "IFC Files (*.ifc);;All Files (*)", options=options)
        if file_name:
            self.load_ifc_file(file_name)

    def load_ifc_file(self, file_name):
        try:
            self.model = ifcopenshell.open(file_name)
            ifc_project = self.get_ifc_project()
            if ifc_project is not None:
                entity_types = self.get_entities_under(ifc_project)
                self.entities_combo.addItems(sorted(entity_types))
                QMessageBox.information(self, "File Loaded", f"Successfully loaded file: {file_name}")
            else:
                QMessageBox.warning(self, "Warning", "No IfcProject found in the file.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")

    def get_ifc_project(self):
        # Find and return the IfcProject instance
        if self.model is None:
            return None
        for entity in self.model.by_type("IfcProject"):
            return entity
        return None

    def get_entities_under(self, ifc_entity):
        entity_types = set()
        self.collect_entity_types(ifc_entity, entity_types)
        return entity_types

    def collect_entity_types(self, ifc_entity, entity_types):
        # Collect all entity types under the given ifc_entity hierarchically
        for attr_name in dir(ifc_entity):
            if attr_name.startswith("Is"):
                related_entities = getattr(ifc_entity, attr_name)()
                if isinstance(related_entities, list):
                    for related_entity in related_entities:
                        if related_entity.is_a() not in entity_types:
                            entity_types.add(related_entity.is_a())
                            self.collect_entity_types(related_entity, entity_types)
                elif isinstance(related_entities, ifcopenshell.entity_instance):
                    if related_entities.is_a() not in entity_types:
                        entity_types.add(related_entities.is_a())
                        self.collect_entity_types(related_entities, entity_types)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = IfcApp()
    mainWin.show()
    sys.exit(app.exec_())
