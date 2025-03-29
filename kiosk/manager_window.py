import json
import sys
import os
import cx_Oracle as oci
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QAbstractItemView
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

class ManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
        loadUi("ui/manager.ui", self)  # UI 로드

        # 시작 준비!
        self.conn = self.get_db_connection()    
        self.cursor = self.conn.cursor()        
        self.menu_data = self.load_json_data()  

        # 버튼 클릭 이벤트 연결
        self.mbtn_check.clicked.connect(self.load_menu_data)  
        self.mbtn_add.clicked.connect(self.add_menu)
        self.mbtn_mod.clicked.connect(self.update_menu)
        self.mbtn_del.clicked.connect(self.delete_menu)
        self.tblMenu.doubleClicked.connect(self.double_click_event)
        
        self.load_menu_data() 

    # 디비 연결
    def get_db_connection(self):
        sid = 'XE'
        host = 'localhost'
        port = 1521
        username = 'kiosk'
        password = '12345'
        return oci.connect(f'{username}/{password}@{host}:{port}/{sid}')

    # menu_data.json 파일 끌고오기
    def load_json_data(self):
        try:
            with open('kiosk/menu_data.json', 'r', encoding='utf-8') as f:  
                return json.load(f) 
        except FileNotFoundError:
            print("menu_data.json 파일을 찾을 수 없습니다.")
            return []

    def check_if_menu_exists(self, menu_name):
        query = "SELECT COUNT(*) FROM MENU WHERE menu_name = :1" 
        self.cursor.execute(query, (menu_name,))
        return self.cursor.fetchone()[0] > 0

    def load_menu_data(self):
        self.tblMenu.setRowCount(len(self.menu_data))
        self.tblMenu.setColumnCount(7)
        self.tblMenu.setHorizontalHeaderLabels(["ID", "Name", "Info", "Price", "Category", "Image", "Status"])

        for i, menu in enumerate(self.menu_data):
            status = "등록됨" if self.check_if_menu_exists(menu['name']) else "등록안됨"
            self.tblMenu.setItem(i, 0, QTableWidgetItem(str(menu['id'])))
            self.tblMenu.setItem(i, 1, QTableWidgetItem(menu['name']))
            self.tblMenu.setItem(i, 2, QTableWidgetItem(menu['info']))
            self.tblMenu.setItem(i, 3, QTableWidgetItem(str(menu['price'])))
            self.tblMenu.setItem(i, 4, QTableWidgetItem(menu['category']))
            self.tblMenu.setItem(i, 5, QTableWidgetItem(menu['image']))
            self.tblMenu.setItem(i, 6, QTableWidgetItem(status))

    def add_menu(self):
        menu_name = self.menu_name_input.text()
        menu_info = self.menu_info_input.toPlainText()
        menu_price = self.menu_price_input.text()
        category = self.category_combobox.currentText()
        image_url = self.menu_image_input.text()

        if menu_name and menu_info and menu_price and category and image_url:
            image_filename = image_url.replace("images/", "")

            if not self.check_if_menu_exists(menu_name):
                self.cursor.execute(
                    """
                    INSERT INTO MENU (menu_name, menu_info, menu_price, category, image)
                    VALUES (:1, :2, :3, :4, :5)
                    """, (menu_name, menu_info, menu_price, category, image_filename))
                self.conn.commit()
                self.load_menu_data()
                QMessageBox.information(self, "성공", "메뉴가 등록되었습니다!")
            else:
                QMessageBox.warning(self, "경고", "이 메뉴는 이미 등록되어 있습니다!")

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
            QMessageBox.information(self, "성공", "수정 성공!")
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
            image_file_name = self.tblMenu.item(selected_row, 5).text()
            image_url = f"images/{image_file_name}"

            self.menu_id_input.setText(menu_id)
            self.menu_name_input.setText(menu_name)
            self.menu_info_input.setPlainText(menu_info)
            self.menu_price_input.setText(menu_price)
            self.category_combobox.setCurrentText(category)

            pixmap = QPixmap(image_url)
            pixmap = pixmap.scaled(self.menu_image_input.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.menu_image_input.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ManagerWindow()
    window.show()
    sys.exit(app.exec_())
