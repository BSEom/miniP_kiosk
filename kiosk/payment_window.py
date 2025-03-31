from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
import re

# UI 파일 로드
payment_form = uic.loadUiType("ui/payment.ui")[0]
cashPay_form = uic.loadUiType("ui/cashPay.ui")[0]
creditPay_form = uic.loadUiType("ui/craditPay.ui")[0]

class paymentWindow(QMainWindow, payment_form):
    def __init__(self, total_order_price, parent=None):  # menu_id 제거
        super().__init__(parent)
        self.setupUi(self)

        self.setWindowTitle("Cafe Kiosk")
        self.setWindowIcon(QIcon("img/coffee-cup.png"))

        # 버튼 클릭 이벤트 연결
        self.cash_btn.clicked.connect(self.openCashWindow)
        self.credit_btn.clicked.connect(self.openCreditWindow)

        self.payMoney_label.setText(f"결제 금액: {total_order_price}원")  # 결제 금액 설정

    def openCashWindow(self):
        self.clearCartTable()  # 장바구니 비우기
        self.cash_window = QMainWindow(self)
        self.cash_ui = cashPay_form()
        self.cash_ui.setupUi(self.cash_window)
        self.cash_window.setWindowTitle("현금 결제")

        # counter_label에 이미지 설정
        icon_path = 'img/cash.png'  # 표시할 이미지 경로
        pixmap = QPixmap(icon_path)
        counter_label = self.cash_window.findChild(QLabel, "counter_label")  # QLabel 찾기

        if counter_label:
            if not pixmap.isNull():
                counter_label.setPixmap(pixmap)  # QLabel에 이미지 설정
                counter_label.setScaledContents(True)  # 이미지 크기 조정
            else:
                print(f"이미지 로드 실패: {icon_path}")
        else:
            print("counter_label 위젯을 찾을 수 없습니다.")

        self.cash_window.show()

    def openCreditWindow(self):
        self.clearCartTable()  # 장바구니 비우기
        self.credit_window = QMainWindow(self)
        self.credit_ui = creditPay_form()
        self.credit_ui.setupUi(self.credit_window)
        self.credit_window.setWindowTitle("카드 결제")
        self.credit_window.show()

        icon_path = 'img/creditPay.png'
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            self.credit_ui.label.setPixmap(pixmap)  # 'label'은 카드 창의 QLabel 이름
            self.credit_ui.label.setScaledContents(True)  # 이미지 크기 조정

        self.credit_window.show()

    def clearCartTable(self):
        if self.parent():  # 부모(menuWindow)가 존재할 때만 실행
            self.parent().allDelRow()  # 부모의 장바구니 초기화 메서드 실행
