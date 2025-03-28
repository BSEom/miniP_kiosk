from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog, QTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
import cx_Oracle as oci
from PyQt5.QtCore import Qt
import sys

# DB 연결 함수
def get_db_connection():
    sid = 'XE'
    host = '210.119.14.76'
    port = 1521
    username = 'kiosk'
    password = '12345'
    return oci.connect(f'{username}/{password}@{host}:{port}/{sid}')

class managerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ui/manager.ui", self)

        # UI에서 menu_image_input가 제대로 연결되었는지 확인
        if hasattr(self, 'menu_image_input'):
            print("menu_image_input 레이블이 정상적으로 로드되었습니다.")
        else:
            print("menu_image_input 레이블이 존재하지 않습니다. UI에서 객체 이름을 확인하세요.")

        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

        self.mbtn_check.clicked.connect(self.check_menu)
        self.mbtn_add.clicked.connect(self.add_menu)
        self.mbtn_mod.clicked.connect(self.update_menu)
        self.mbtn_del.clicked.connect(self.delete_menu)
        self.mbtn_apply.clicked.connect(self.apply_changes)
        self.mbtn_back.clicked.connect(self.revert_changes)
        self.tblMenu.doubleClicked.connect(self.double_click_event)

        self.load_menu_data()
        self.previous_data = []

        # 메뉴 설명 부분을 QTextEdit로 변경
        self.menu_info_input = QTextEdit(self)
        self.menu_info_input.setGeometry(150, 150, 300, 100)  # 위치와 크기를 설정

    def load_menu_data(self, category=None):
        query = "SELECT menu_id, menu_name, menu_info, menu_price, category, image FROM MENU"
        if category and category != '선택':
            query += " WHERE category = :1"
            self.cursor.execute(query, (category,))
        else:
            self.cursor.execute(query)

        rows = self.cursor.fetchall()
        self.tblMenu.setRowCount(len(rows))
        self.tblMenu.setColumnCount(6)  # 이미지 추가
        self.tblMenu.setHorizontalHeaderLabels(["ID", "Name", "Info", "Price", "Category", "Image"])

        for i, row in enumerate(rows):
            for j, item in enumerate(row):
                table_item = QTableWidgetItem(str(item))
                table_item.setFlags(table_item.flags() & ~Qt.ItemIsEditable)
                self.tblMenu.setItem(i, j, table_item)

    def check_menu(self):
        category = self.category_combobox.currentText()
        self.load_menu_data(category)

    def add_menu(self):
        menu_name = self.menu_name_input.text()
        menu_info = self.menu_info_input.toPlainText()  # QTextEdit의 텍스트를 가져옴
        menu_price = self.menu_price_input.text()
        category = self.category_combobox.currentText()
        image_url = self.menu_image_input.text()

        if menu_name and menu_info and menu_price and category and image_url:
            self.cursor.execute(
                """
                INSERT INTO MENU (menu_name, menu_info, menu_price, category, image)
                VALUES (:1, :2, :3, :4, :5)
                """, (menu_name, menu_info, menu_price, category, image_url))
            self.conn.commit()
            self.load_menu_data()

    def update_menu(self):
        selected_row = self.tblMenu2.currentRow()
        if selected_row >= 0:
            menu_id = self.tblMenu2.item(selected_row, 0).text()
            menu_name = self.menu_name_input.text()
            menu_info = self.menu_info_input.toPlainText()  # QTextEdit의 텍스트를 가져옴
            menu_price = self.menu_price_input.text()
            category = self.category_combobox.currentText()
            image_url = self.menu_image_input.text()

            self.cursor.execute(
                """
                UPDATE MENU
                SET menu_name = :1, menu_info = :2, menu_price = :3, category = :4, image = :5
                WHERE menu_id = :6
                """, (menu_name, menu_info, menu_price, category, image_url, menu_id))
            self.conn.commit()
            self.load_menu_data()

    def delete_menu(self):
        selected_row = self.tblMenu2.currentRow()
        if selected_row >= 0:
            menu_id = self.tblMenu2.item(selected_row, 0).text()
            self.cursor.execute("DELETE FROM MENU WHERE menu_id = :1", (menu_id,))
            self.conn.commit()
            self.load_menu_data()

    def double_click_event(self):
        selected_row = self.tblMenu.currentRow()
        if selected_row >= 0:
            menu_id = self.tblMenu.item(selected_row, 0).text()
            menu_name = self.tblMenu.item(selected_row, 1).text()
            menu_info = self.tblMenu.item(selected_row, 2).text()
            menu_price = self.tblMenu.item(selected_row, 3).text()
            category = self.tblMenu.item(selected_row, 4).text()
            image_file_name = self.tblMenu.item(selected_row, 5).text()  # 디비에서 가져온 이미지 파일명

            # 이미지 경로는 "images/디비 이미지 파일명" 형태로 수정
            image_url = f"images/{image_file_name}"

            # 상태 페이지의 입력 필드에 값 설정
            self.menu_name_input.setText(menu_name)
            self.menu_info_input.setPlainText(menu_info)  # QTextEdit에 텍스트 설정
            self.menu_price_input.setText(menu_price)
            self.category_combobox.setCurrentText(category)

            # 이미지 경로만 텍스트로 입력
            self.menu_image_input.setText(image_url)

            # 이미지 띄우기 (QLabel에 이미지를 표시)
            pixmap = QPixmap(image_url)

            # QLabel 크기 맞게 이미지 리사이징
            pixmap = pixmap.scaled(self.menu_image_input.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

            if hasattr(self, 'menu_image_input'):  # menu_image_input이 QLabel로 로드되었는지 확인
                self.menu_image_input.setPixmap(pixmap)  # 이미지 띄우기
            else:
                print("menu_image_input 레이블이 존재하지 않습니다.")

            # 이전 데이터 저장 (수정 시 복원용)
            self.previous_data = [menu_id, menu_name, menu_info, menu_price, category, image_file_name]

    def apply_changes(self):
        selected_row = self.tblMenu2.currentRow()
        if selected_row >= 0:
            menu_id = self.tblMenu2.item(selected_row, 0).text()
            menu_name = self.tblMenu2.item(selected_row, 1).text()
            menu_info = self.tblMenu2.item(selected_row, 2).text()
            menu_price = self.tblMenu2.item(selected_row, 3).text()
            category = self.tblMenu2.item(selected_row, 4).text()
            image_url = self.tblMenu2.item(selected_row, 5).text()

            self.cursor.execute(
                """
                UPDATE MENU
                SET menu_name = :1, menu_info = :2, menu_price = :3, category = :4, image = :5
                WHERE menu_id = :6
                """, (menu_name, menu_info, menu_price, category, image_url, menu_id))
            self.conn.commit()
            self.load_menu_data()

    def revert_changes(self):
        if self.previous_data:
            for col, text in enumerate(self.previous_data):
                self.tblMenu2.setItem(0, col, QTableWidgetItem(text))

    def closeEvent(self, event):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = managerWindow()
    window.show()
    sys.exit(app.exec_())
