from Operations.idsOps import IdsOps

version=IdsOps.getIdsVersionXML(r"C:\Users\ivanf\OneDrive\Desktop\Masterarbeit\0-Repo_Thesis\BIMQA_Quick_Checker\temp_files\TempIds.ids")
print(version)
diccionario= IdsOps.parseXmlToDict(r"C:\Users\ivanf\OneDrive\Desktop\Masterarbeit\0-Repo_Thesis\BIMQA_Quick_Checker\temp_files\TempIds.ids")
print(diccionario)

# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget, QPushButton, QLabel, QFileDialog, QListWidgetItem


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle('File List Example')

#         # Main widget and layout
#         main_widget = QWidget()
#         self.setCentralWidget(main_widget)
#         layout = QVBoxLayout(main_widget)

#         # List view widget
#         self.list_view = QListWidget()
#         layout.addWidget(self.list_view)

#         # Button to add files
#         self.add_button = QPushButton('Add Files')
#         self.add_button.clicked.connect(self.add_files)
#         layout.addWidget(self.add_button)

#         # Button to show selected label
#         self.show_label_button = QPushButton('ShowLabel')
#         self.show_label_button.clicked.connect(self.update_label)
#         layout.addWidget(self.show_label_button)

#         # Label to display selected file path
#         self.selected_label = QLabel('Selected File:')
#         layout.addWidget(self.selected_label)

#     def add_files(self):
#         file_dialog = QFileDialog(self)
#         file_dialog.setFileMode(QFileDialog.ExistingFiles)

#         if file_dialog.exec_():
#             file_paths = file_dialog.selectedFiles()
#             for file_path in file_paths:
#                 item = QListWidgetItem(file_path)  # Create a QListWidgetItem
#                 self.list_view.addItem(item)

#     def update_label(self):
#         selected_items = self.list_view.selectedItems()
#         if selected_items:
#             selected_item = selected_items[0]
#             self.selected_label.setText(f'Selected File: {selected_item.text()}')
#         else:
#             self.selected_label.setText('Selected File:')

#     def closeEvent(self, event):
#         # Override closeEvent to clean up resources if needed
#         super().closeEvent(event)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main_window = MainWindow()
#     main_window.show()
#     sys.exit(app.exec_())
