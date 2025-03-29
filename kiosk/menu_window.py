from PyQt5.QtWidgets import QMainWindow, QGridLayout, QPushButton, QWidget, QVBoxLayout, QLabel, QTableWidgetItem, QTableWidget, QSpinBox, QMessageBox, QDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5 import uic
import cx_Oracle as oci
import os
from exPrice_window import expriceWindow
from payment_window import paymentWindow

menu_form = uic.loadUiType("ui/menu.ui")[0]

sid = 'XE'
# host = '210.119.14.76'
host = 'localhost'
port = 1521
username = 'kiosk'
password = '12345'

# 메뉴 버튼 클릭 시, expriceWindow로 메뉴 데이터 전달 및 표시
class menuWindow(QMainWindow, menu_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.loadCategories()
        # self.loadMenuData()   # 카테고리 로드한 후에 카테고리별로 실행해야돼서 뺐음

        #self.edit_btn = self.findChild(QPushButton, "edit_btn")
        self.home_btn.clicked.connect(self.close)
        self.allDel_btn.clicked.connect(self.allDelRow)
        
    def initUI(self):
        self.setWindowTitle('Cafe Kiosk')
        self.setWindowIcon(QIcon('img/coffee-cup.png'))

        # 테이블 컬럼명
        self.cart_tbl.setColumnCount(3)
        self.cart_tbl.setHorizontalHeaderLabels(['메뉴명', '수량', '가격'])
        self.cart_tbl.setRowCount(0)

        # 삭제 버튼을 메뉴에 추가하는 부분 (initUI에서)
        self.del_btn = self.findChild(QPushButton, "del_btn")
        # 삭제 버튼 클릭 -> 행 삭제
        self.del_btn.clicked.connect(self.delRow)
        # 수정 버튼 클릭 -> 행 수정
        self.edit_btn.clicked.connect(self.editRow)
        # 전체 삭제 버튼 클릭 -> 테이블 초기화
        self.all_del_btn = self.findChild(QPushButton, "all_del_btn")

        # 결제 버튼 클릭 -> 결제 페이지로 이동
        self.pay_btn.clicked.connect(self.paymentWindow)

    # 카테고리 목록을 DB에서 가져와서 탭 동적 생성
    def loadCategories(self):
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        query = 'SELECT DISTINCT category FROM menu'    # 카테고리 중복 제거
        cursor.execute(query)
        categories = [row[0] for row in cursor]  # 카테고리 목록

        cursor.close()
        conn.close()
        
        tab_count = self.tabWidget.count()

        # 각 카테고리에 대한 탭 추가
        for i in range(min(tab_count, len(categories))):
            category = categories[i]
            self.setCategoryTab(i, category)
            
    # 카테고리 탭에 적용용
    def setCategoryTab(self, index, category):
        """
        기존의 특정 탭(index)에 카테고리명을 설정하고 해당 카테고리 메뉴 불러오기
        """
        # 탭 이름 변경
        self.tabWidget.setTabText(index, category)

        scroll_widget = self.tabWidget.widget(index).findChild(QWidget, f"scrollAreaWidgetContents_{index+1}")

        # if not scroll_widget:
        #     print(f"scrollWidgetContents_{index+1} 찾을 수 없음!")
        #     return  # 에러 방지

        layout = scroll_widget.findChild(QGridLayout, f"gridLayout_{index+8}")

        if not layout:
            print(f"gridLayout_{index+8}")
            layout = QGridLayout(scroll_widget)
            scroll_widget.setLayout(layout)
            
        self.loadMenuData(category, layout)
    
    # 카테고리별 메뉴를 DB에서 가져와서 버튼 동적 생성
    def loadMenuData(self, category, layout):
        # 기존 메뉴 항목 제거 (중복 추가 방지)
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        query = 'SELECT menu_id, menu_name, image FROM menu WHERE category = :category'
        cursor.execute(query, {'category': category})

        # 메뉴 데이터를 저장할 리스트
        menu_data = cursor.fetchall()
        cursor.close()
        conn.close()

        # 메뉴 테이블 생성
        # self.menuTable(menu_data, layout)
        
        # 이 아래 코드는 일단 지우지말아주세요... -정민
        for i, (menu_id, menu_name, image_filename) in enumerate(menu_data):
            menu_item = self.createMenuWidget(menu_id, image_filename, menu_name)
            row, col = divmod(i, 3)  # 3열 기준 배치
            layout.addWidget(menu_item, row, col)

    def createMenuWidget(self, menu_id, image_filename, text):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_folder = os.path.join(base_dir, "../images/")

        # # image_filename이 None인 경우 기본 이미지 설정
        # if not image_filename:
        #     print(f"menu_id {menu_id}의 image_filename이 None입니다. 기본 이미지를 사용합니다.")
        #     image_filename = "default.png"  # 기본 이미지 파일 이름

        image_path = os.path.normpath(os.path.join(image_folder, image_filename))

        # 이미지 경로 디버깅
        # print(f"이미지 경로: {image_path}")

        menu_item = QWidget()
        layout = QVBoxLayout(menu_item)
        layout.setAlignment(Qt.AlignCenter)

        button = QPushButton()
        button.setFixedSize(95, 95)
        pixmap = QPixmap(image_path)

        if not pixmap.isNull():
            resized_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            button.setIcon(QIcon(resized_pixmap))
            button.setIconSize(QSize(80, 80))
        else:
            print(f"이미지 로드 실패: {image_path}")
            # # 기본 이미지를 사용
            # default_image_path = os.path.normpath(os.path.join(image_folder, "default.png"))
            # pixmap = QPixmap(default_image_path)
            # if not pixmap.isNull():
            #     resized_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            #     button.setIcon(QIcon(resized_pixmap))
            #     button.setIconSize(QSize(80, 80))
            # else:
            #     print(f"기본 이미지도 로드 실패: {default_image_path}")

        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)
        label.setFixedSize(95, 50)

        layout.addWidget(button)
        layout.addWidget(label)

        button.clicked.connect(lambda _, mid=menu_id: self.showExpriceWindow(mid))

        return menu_item

    def showExpriceWindow(self, menu_id):
        self.window_4 = expriceWindow(menu_id=menu_id, parent=self)  # 부모 창을 전달
        self.window_4.show()

    def addMenuTable(self, menu_name, quantity, menu_price):
        row_position = self.cart_tbl.rowCount()
        self.cart_tbl.insertRow(row_position)
        self.cart_tbl.setItem(row_position, 0, QTableWidgetItem(menu_name))
        self.cart_tbl.setItem(row_position, 1, QTableWidgetItem(str(quantity)))
        self.cart_tbl.setItem(row_position, 2, QTableWidgetItem(str(menu_price)))

    def delRow(self):
        selected_row = self.cart_tbl.currentRow()  # 현재 선택된 행

        if selected_row >= 0:  # 선택된 행이 있을 때만 삭제
            # 해당 행 삭제
            self.cart_tbl.removeRow(selected_row)
        else:
            print("삭제할 항목을 선택하세요.")

    def allDelRow(self):
        # 테이블 초기화 (모든 행 삭제)
        self.cart_tbl.setRowCount(0)

    def editRow(self):
        # 수량 변경
        selected_row = self.cart_tbl.currentRow()  # 현재 선택된 행
        if selected_row >= 0:  # 선택된 행이 있을 때만 수정
            menu_name = self.cart_tbl.item(selected_row, 0).text()  # 메뉴명 가져오기
            quantity = int(self.cart_tbl.item(selected_row, 1).text())  # 기존 수량 가져오기
            price_text = self.cart_tbl.item(selected_row, 2).text()  # 기존 가격 가져오기

            # 가격에서 숫자만 추출 (가격이 "1500" 형태일 경우)
            menu_price = int(price_text.replace("원", "")) // quantity  # 메뉴 가격 계산

            # 수량을 수정할 수 있는 다이얼로그 호출
            dialog = QDialog(self)
            dialog.setWindowTitle("수량 수정")
            
            layout = QVBoxLayout(dialog)
            
            # 수량을 수정할 수 있는 SpinBox
            spin_box = QSpinBox(dialog)
            spin_box.setValue(quantity)  # 기존 수량 설정
            layout.addWidget(QLabel("수량을 변경하세요"))
            layout.addWidget(spin_box)

            confirm_btn = QPushButton("확인", dialog)
            layout.addWidget(confirm_btn)

            # 확인 버튼 클릭 시 동작
            def on_confirm():
                new_quantity = spin_box.value()
                if new_quantity == 0:
                    QMessageBox.warning(dialog, "경고", "수량이 0이면 메뉴를 추가할 수 없습니다.")
                else:
                    # 수정된 수량에 맞는 새로운 가격 계산
                    new_price = menu_price * new_quantity

                    # 수정된 수량과 가격을 테이블에 반영
                    self.cart_tbl.setItem(selected_row, 1, QTableWidgetItem(str(new_quantity)))  # 수량 업데이트
                    self.cart_tbl.setItem(selected_row, 2, QTableWidgetItem(f"{new_price}원"))  # 가격 업데이트

                    dialog.accept()  # 다이얼로그 닫기

            confirm_btn.clicked.connect(on_confirm)
            
            dialog.exec_()  # 다이얼로그 실행

    def paymentWindow(self):
        try:
            # DB 연결
            conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
            cursor = conn.cursor()

            # 테이블 데이터 가져오기
            row_count = self.cart_tbl.rowCount()
            if row_count == 0:
                QMessageBox.warning(self, "경고", "결제할 메뉴가 없습니다.")
                return

            # 새로운 order_id 생성
            cursor.execute("SELECT ORDER_ID_SEQ.NEXTVAL FROM dual")  # order_id를 생성하는 시퀀스
            order_id = cursor.fetchone()[0]

            # 전체 주문 가격 계산
            total_order_price = 0
            for row in range(row_count):
                menu_name = self.cart_tbl.item(row, 0).text()  # 메뉴명
                quantity = int(self.cart_tbl.item(row, 1).text())  # 수량
                price_text = self.cart_tbl.item(row, 2).text()  # 가격 텍스트

                # 가격에서 "원", "," 및 공백을 제거하고 숫자로 변환
                try:
                    menu_price = int(price_text.replace("원", "").replace(",", "").strip())
                except ValueError:
                    raise ValueError(f"가격 '{price_text}'을 숫자로 변환할 수 없습니다.")

                total_price = menu_price  # 총 가격 계산
                total_order_price += total_price  # 전체 주문 가격에 더하기

            # order 테이블에 데이터 삽입
            cursor.execute("""
                INSERT INTO ORDER_TABLE (ORDER_ID, ORDER_PRICE, ORDER_DATE)
                VALUES (:order_id, :order_price, SYSDATE)
            """, {"order_id": order_id, "order_price": total_order_price})

            # orderinfo 테이블에 데이터 삽입
            for row in range(row_count):
                menu_name = self.cart_tbl.item(row, 0).text()  # 메뉴명
                quantity = int(self.cart_tbl.item(row, 1).text())  # 수량
                price_text = self.cart_tbl.item(row, 2).text()  # 가격 텍스트

                # 가격에서 "원", "," 및 공백을 제거하고 숫자로 변환
                try:
                    menu_price = int(price_text.replace("원", "").replace(",", "").strip())
                except ValueError:
                    raise ValueError(f"가격 '{price_text}'을 숫자로 변환할 수 없습니다.")

                total_price = menu_price * quantity  # 총 가격 계산

                # 메뉴명을 이용해 MENU_ID 가져오기
                cursor.execute("SELECT MENU_ID FROM MENU WHERE MENU_NAME = :menu_name", {"menu_name": menu_name})
                result = cursor.fetchone()

                if result:
                    menu_id = result[0]  # MENU_ID 가져오기

                    # orderinfo_id 생성
                    cursor.execute("SELECT ORDERINFO_ID_SEQ.NEXTVAL FROM dual")
                    orderinfo_id = cursor.fetchone()[0]

                    # orderinfo 테이블에 데이터 삽입
                    cursor.execute("""
                        INSERT INTO ORDERINFO (ORDERINFO_ID, ORDER_ID, MENU_ID, PRICE, COUNT)
                        VALUES (:orderinfo_id, :order_id, :menu_id, :price, :count)
                    """, {
                        "orderinfo_id": orderinfo_id,
                        "order_id": order_id,
                        "menu_id": menu_id,
                        "price": menu_price,
                        "count": quantity
                    })

            # 트랜잭션 커밋
            conn.commit()

            QMessageBox.information(self, "성공", "주문이 완료되었습니다.")
            self.payment_window = paymentWindow(self)
            self.payment_window.show()

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "오류", f"주문 처리 중 오류가 발생했습니다: {str(e)}")

        finally:
            cursor.close()
            conn.close()





