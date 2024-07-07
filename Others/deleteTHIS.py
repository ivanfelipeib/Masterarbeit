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
        self.combo_instance.currentIndexChanged.connect(self.update_attributes)
        layout.addWidget(self.instance_label)
        layout.addWidget(self.combo_instance)

        # Attribute combobox and label
        self.attribute_label = QLabel('Attribute:')
        self.combo_attributes = QComboBox()
        self.combo_attributes.currentIndexChanged.connect(self.update_result)
        layout.addWidget(self.attribute_label)
        layout.addWidget(self.combo_attributes)

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
            entities.add(entity.is_a())
        self.combo_entity.addItems(sorted(entities))

    def update_instances(self):
        self.combo_instance.clear()
        entity_type = self.combo_entity.currentText()
        if entity_type:
            instances = self.model.by_type(entity_type)
            instance_ids = [str(instance.id()) for instance in instances]
            self.combo_instance.addItems(instance_ids)

    def update_attributes(self):
        self.combo_attributes.clear()
        instance_id = self.combo_instance.currentText()
        if instance_id:
            instance = self.model.by_id(int(instance_id))
            attributes = [attr for attr in instance.get_info(recursive=True).keys()]
            self.combo_attributes.addItems(attributes)

    def update_result(self):
        instance_id = self.combo_instance.currentText()
        attribute = self.combo_attributes.currentText()
        if instance_id and attribute:
            instance = self.model.by_id(int(instance_id))
            value = getattr(instance, attribute, None)
            self.txt_result.setText(str(value))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = IFCApp()
    ex.show()
    sys.exit(app.exec_())
