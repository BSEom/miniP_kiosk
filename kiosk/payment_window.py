from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic

# UI 파일 로드
payment_form = uic.loadUiType("ui/payment.ui")[0]
cashPay_form = uic.loadUiType("ui/cashPay.ui")[0]
creditPay_form = uic.loadUiType("ui/craditPay.ui")[0]

class paymentWindow(QMainWindow, payment_form):
    def __init__(self, menu_id, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.setWindowTitle("Cafe Kiosk")
        self.setWindowIcon(QIcon("img/coffee-cup.png"))

        # 버튼 클릭 이벤트 연결
        self.cash_btn.clicked.connect(self.openCashWindow)
        self.credit_btn.clicked.connect(self.openCreditWindow)

    def openCashWindow(self):
        # 현금 결제 창 열기
        self.cash_window = QMainWindow(self)
        self.cash_ui = cashPay_form()
        self.cash_ui.setupUi(self.cash_window)
        self.cash_window.setWindowTitle("현금 결제")
        self.cash_window.show()

    def openCreditWindow(self):
        # 카드 결제 창 열기
        self.credit_window = QMainWindow(self)
        self.credit_ui = creditPay_form()
        self.credit_ui.setupUi(self.credit_window)
        self.credit_window.setWindowTitle("카드 결제")
        self.credit_window.show()

        icon_path = 'img\creditPay.png'
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            self.credit_ui.label.setPixmap(pixmap)  # 'label'은 카드 창의 QLabel 이름
            self.credit_ui.label.setScaledContents(True)  # 이미지 크기 조정

        self.credit_window.show()