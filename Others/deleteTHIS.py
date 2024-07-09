import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QLineEdit, QVBoxLayout, QDialog, QPlainTextEdit
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Nested Dictionary Viewer")
        self.setGeometry(100, 100, 400, 200)

        self.nested_dict = {
            'item1': 'value1',
            'item2': {
                'subitem1': 'subvalue1',
                'subitem2': 'subvalue2'
            },
            'item3': 'value3'
        }

        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(50, 50, 200, 30)
        self.comboBox.addItems(self.nested_dict.keys())
        self.comboBox.currentIndexChanged.connect(self.display_value)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(50, 100, 300, 30)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.mousePressEvent = self.handle_link_click

    def display_value(self):
        key = self.comboBox.currentText()
        value = self.nested_dict[key]
        
        if isinstance(value, dict):
            self.lineEdit.setText('Click to view dictionary')
            self.lineEdit.setCursor(QCursor(Qt.PointingHandCursor))
            self.current_value = value
        else:
            self.lineEdit.setText(value)
            self.lineEdit.setCursor(QCursor(Qt.IBeamCursor))

    def handle_link_click(self, event):
        if isinstance(self.current_value, dict):
            self.show_dictionary()

    def show_dictionary(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Dictionary Contents")
        
        plainTextEdit = QPlainTextEdit(dialog)
        formatted_text = self.format_dictionary(self.current_value)
        plainTextEdit.setPlainText(formatted_text)
        plainTextEdit.setReadOnly(True)
        
        layout = QVBoxLayout(dialog)
        layout.addWidget(plainTextEdit)
        dialog.setLayout(layout)
        
        dialog.exec_()

    def format_dictionary(self, dictionary, level=0):
        formatted_text = ""
        for key, value in dictionary.items():
            if isinstance(value, dict):
                formatted_text += f"{' ' * (level * 4)}{key}:\n"
                formatted_text += self.format_dictionary(value, level + 1)
            else:
                formatted_text += f"{' ' * (level * 4)}{key}: {value}\n"
        return formatted_text

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
