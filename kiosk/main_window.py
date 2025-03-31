from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
from menu_window import menuWindow
from check_window import checkWindow


main_form = uic.loadUiType("ui/kiosk.ui")[0]

class mainWindow(QMainWindow, main_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Cafe Kiosk")
        self.setWindowIcon(QIcon("img/coffee-cup.png"))

        self.image_label = self.findChild(QLabel, "homeImg_label")
        if self.image_label:
            pixmap = QPixmap("img/home.png")  # 표시할 이미지 경로
            if not pixmap.isNull():
                self.image_label.setPixmap(pixmap)
                self.image_label.setScaledContents(True)  # 이미지 크기 조정
            else:
                print("이미지 로드 실패: img/main_image.png")
        else:
            print("image_label 위젯을 찾을 수 없습니다.")

        self.start_btn.clicked.connect(self.menuWindow)
        self.manager_btn.clicked.connect(self.checkWindow)
        self.show()




    def menuWindow(self):
        self.window_2 = menuWindow()
        self.window_2.show()

    def checkWindow(self):
        self.window_4 = checkWindow()
        self.window_4.show()





