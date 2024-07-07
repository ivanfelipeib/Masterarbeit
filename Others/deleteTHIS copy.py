import sys
import ifcopenshell
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit, QFileDialog
)
from PyQt5.QtCore import Qt

class IFCApp(QWidget):
    def __init__(self):
        super().__init__()

        self.model = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Import IFC button
        self.import_ifc_btn = QPushButton('Import IFC')
        self.import_ifc_btn.clicked.connect(self.import_ifc)
        layout.addWidget(self.import_ifc_btn)

        # Entity combobox and label
        self.entity_label = QLabel('Entity:')
        self.combo_entity = QComboBox()
        self.combo_entity.currentIndexChanged.connect(self.update_instances)
        layout.addWidget(self.entity_label)
        layout.addWidget(self.combo_entity)

        # Instance combobox and label
        self.instance_label = QLabel('Instance:')
        self.combo_instance = QComboBox()
        self.combo_instance.currentIndexChanged.connect(self.update_psets)
        layout.addWidget(self.instance_label)
        layout.addWidget(self.combo_instance)

        # Property Stes combobox and label
        self.pset_label = QLabel('PSets:')
        self.combo_psets = QComboBox()
        self.combo_psets.currentIndexChanged.connect(self.update_props)
        layout.addWidget(self.pset_label)
        layout.addWidget(self.combo_psets)

        # Properties combobox and label
        self.props_label = QLabel('Properties:')
        self.combo_props = QComboBox()
        self.combo_props.currentIndexChanged.connect(self.update_result)
        layout.addWidget(self.props_label)
        layout.addWidget(self.combo_props)

        # Result QLineEdit and label
        self.result_label = QLabel('Result:')
        self.txt_result = QLineEdit()
        layout.addWidget(self.result_label)
        layout.addWidget(self.txt_result)

        self.setLayout(layout)
        self.setWindowTitle('IFC Viewer')

    def import_ifc(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open IFC File", "", "IFC Files (*.ifc)", options=options)
        if file_name:
            self.model = ifcopenshell.open(file_name)
            self.load_entities()

    def load_entities(self):
        self.combo_entity.clear()
        entities = set()
        for entity in self.model.by_type('IfcRoot'):
            if hasattr(entity, 'IsDefinedBy'): #https://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2_TC1/HTML/link/ifcobject.htm Assignment of property sets : IsDefinedBy - a definition relationship IfcRelDefinesByProperties that assignes property set definitions to the object occurrence.
                entities.add(entity.is_a())
        self.combo_entity.addItems(sorted(entities))

    def update_instances(self):
        self.combo_instance.clear()
        entity_type = self.combo_entity.currentText()
        if entity_type:
            instances = self.model.by_type(entity_type)
            instance_ids = [str(instance.get_info()["GlobalId"]) for instance in instances]
            self.combo_instance.addItems(instance_ids)

    def update_psets(self):
        self.combo_psets.clear()
        instance_id = self.combo_instance.currentText()
        if instance_id:
            instance = self.model.by_guid(instance_id)
            # Iterate through the IsDefinedBy relationships
            self.psets_dict={}
            for definition in instance.IsDefinedBy:
                if definition.is_a('IfcRelDefinesByProperties'):
                    property_set = definition.RelatingPropertyDefinition
                    if property_set.is_a('IfcPropertySet'):
                        props_dict={}
                        for prop in property_set.HasProperties:
                            prop_value = '<not handled>'
                            if prop.is_a('IfcPropertySingleValue'):
                                prop_value = str(prop.NominalValue.wrappedValue)
                                props_dict[prop.Name]= prop_value
                        self.psets_dict[property_set.Name] = props_dict

            self.combo_psets.addItems(self.psets_dict.keys())
    
    def update_props(self):
        self.combo_props.clear()
        pset_name = self.combo_psets.currentText()
        if pset_name:
            props_names = [prop for prop in self.psets_dict[pset_name].keys()]
            self.combo_props.addItems(props_names)

    def update_result(self):
        pset_name = self.combo_psets.currentText()
        prop_name= self.combo_props.currentText()
        if prop_name and pset_name:
            value = self.psets_dict[pset_name][prop_name]
            self.txt_result.setText(str(value))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = IFCApp()
    ex.show()
    sys.exit(app.exec_())
