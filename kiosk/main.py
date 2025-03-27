import sys
from PyQt5.QtWidgets import QApplication
from main_window import mainWindow

# 전체 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = mainWindow()
    app.exec_()
