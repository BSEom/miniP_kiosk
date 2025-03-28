import json
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QLineEdit, QComboBox, QLabel, QAbstractItemView
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
import cx_Oracle as oci
from PyQt5.QtCore import Qt
import os

# DB 연결 함수
def get_db_connection():
    sid = 'XE'
    host = '210.119.14.76'
    port = 1521
    username = 'kiosk'
    password = '12345'
    return oci.connect(f'{username}/{password}@{host}:{port}/{sid}')

# menu_data.json에서 데이터를 로드하는 함수
def load_json_data():
    try:
        with open('kiosk/menu_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("menu_data.json 파일을 찾을 수 없습니다.")
        return []

# UI 클래스 정의
class managerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ui/manager.ui", self)  # UI 로드

        self.conn = get_db_connection()  # DB 연결
        self.cursor = self.conn.cursor()

        # 버튼 클릭 시 연결
        self.mbtn_check.clicked.connect(self.check_menu)
        self.mbtn_add.clicked.connect(self.add_menu)
        self.mbtn_mod.clicked.connect(self.update_menu)
        self.mbtn_del.clicked.connect(self.delete_menu)
        self.mbtn_back.clicked.connect(self.revert_changes)
        self.tblMenu.doubleClicked.connect(self.double_click_event)

        # 상태 페이지 UI 요소 초기화
        self.previous_data = []

        # 메뉴 데이터 로드
        self.menu_data = load_json_data()  # 메뉴 데이터 로드
        self.load_menu_data()

    # DB에서 메뉴가 등록되었는지 확인하는 함수
    def check_if_menu_exists(self, menu_name):
        query = "SELECT COUNT(*) FROM MENU WHERE menu_name = :1"
        self.cursor.execute(query, (menu_name,))
        result = self.cursor.fetchone()
        return result[0] > 0

    def load_menu_data(self):
        # 테이블 설정
        self.tblMenu.setRowCount(len(self.menu_data))
        self.tblMenu.setColumnCount(7)
        self.tblMenu.setHorizontalHeaderLabels(["ID", "Name", "Info", "Price", "Category", "Image", "Status"])

        for i, menu in enumerate(self.menu_data):
            menu_id = str(menu['id'])
            menu_name = menu['name']
            menu_info = menu['info']
            menu_price = menu['price']
            category = menu['category']
            image_url = menu['image']

            # DB에 메뉴가 존재하는지 확인
            status = "등록됨" if self.check_if_menu_exists(menu_name) else "등록안됨"

            self.tblMenu.setItem(i, 0, QTableWidgetItem(menu_id))
            self.tblMenu.setItem(i, 1, QTableWidgetItem(menu_name))
            self.tblMenu.setItem(i, 2, QTableWidgetItem(menu_info))
            self.tblMenu.setItem(i, 3, QTableWidgetItem(str(menu_price)))
            self.tblMenu.setItem(i, 4, QTableWidgetItem(category))
            self.tblMenu.setItem(i, 5, QTableWidgetItem(image_url))
            self.tblMenu.setItem(i, 6, QTableWidgetItem(status))

    def check_menu(self):
        self.load_menu_data()

    def add_menu(self):
        menu_name = self.menu_name_input.text()
        menu_info = self.menu_info_input.toPlainText()
        menu_price = self.menu_price_input.text()
        category = self.category_combobox.currentText()
        image_url = self.menu_image_input.text()

        if menu_name and menu_info and menu_price and category and image_url:
            # 이미지 URL에서 파일명만 추출 (예: "images/IMG_1740122649397.png" -> "IMG_1740122649397.png")
            image_filename = image_url.replace("images/", "")

            # DB에서 해당 메뉴가 이미 등록되어 있는지 확인
            if not self.check_if_menu_exists(menu_name):  # 등록 안된 메뉴일 경우
                # 메뉴가 삭제된 경우 DB에 추가
                self.cursor.execute(
                    """
                    INSERT INTO MENU (menu_name, menu_info, menu_price, category, image)
                    VALUES (:1, :2, :3, :4, :5)
                    """, (menu_name, menu_info, menu_price, category, image_filename))
                self.conn.commit()
                self.load_menu_data()

                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setText("메뉴가 등록되었습니다!")
                msg_box.setWindowTitle("성공")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
            else:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("이 메뉴는 이미 등록되어 있습니다!")
                msg_box.setWindowTitle("경고")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()


    def update_menu(self):
        selected_row = self.tblMenu.currentRow()
        if selected_row >= 0:
            menu_id = self.tblMenu.item(selected_row, 0).text()
            menu_name = self.menu_name_input.text()
            menu_info = self.menu_info_input.toPlainText()
            menu_price = self.menu_price_input.text()
            category = self.category_combobox.currentText()
            image_url = self.tblMenu.item(selected_row, 5).text()

            self.cursor.execute(
                """
                UPDATE MENU
                SET menu_name = :1, menu_info = :2, menu_price = :3, category = :4, image = :5
                WHERE menu_id = :6
                """, (menu_name, menu_info, menu_price, category, image_url, menu_id))
            self.conn.commit()

            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText("수정 성공!")
            msg_box.setWindowTitle("성공")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()

            self.load_menu_data()

    def delete_menu(self):
        selected_row = self.tblMenu.currentRow()
        if selected_row >= 0:
            menu_id = self.tblMenu.item(selected_row, 0).text()
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
            image_file_name = self.tblMenu.item(selected_row, 5).text()  # 이미지 파일명

            # 경로와 파일명을 결합하여 이미지 URL 생성
            image_url = f"images/{image_file_name}"  # 예: images/IMG_1740122649397.png

            self.menu_id_input.setText(menu_id)
            self.menu_name_input.setText(menu_name)
            self.menu_info_input.setPlainText(menu_info)
            self.menu_price_input.setText(menu_price)
            self.category_combobox.setCurrentText(category)

            # 조회 페이지에서는 비활성화 처리 (수정 불가능)
            self.tblMenu.setEditTriggers(QAbstractItemView.NoEditTriggers)

            # 이미지 경로로 QPixmap 생성
            pixmap = QPixmap(image_url)

            # QLabel에 이미지 설정 (이미지 크기 조정 필요 시)
            pixmap = pixmap.scaled(self.menu_image_input.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.menu_image_input.setPixmap(pixmap)

    def revert_changes(self):
        # 수정 전 상태로 되돌리는 로직을 추가하시면 됩니다.
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = managerWindow()
    window.show()
    sys.exit(app.exec_())
