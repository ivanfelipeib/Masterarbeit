from PyQt5.QtWidgets import QApplication
from windows import MainWindow
import sys

#Initialize the app
app= QApplication(sys.argv)
UIWindow = MainWindow()
UIWindow.show()
app.exec_()   

