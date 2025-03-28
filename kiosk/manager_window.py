import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog, QTextEdit, QMessageBox, QLineEdit, QComboBox, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
import cx_Oracle as oci
from PyQt5.QtCore import Qt

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
        loadUi("ui/manager.ui", self)  # UI 로드

        self.conn = get_db_connection()  # DB 연결
        self.cursor = self.conn.cursor()

        # 버튼 클릭 시 연결
        self.mbtn_check.clicked.connect(self.check_menu)
        self.mbtn_add.clicked.connect(self.add_menu)
        self.mbtn_mod.clicked.connect(self.update_menu)
        self.mbtn_del.clicked.connect(self.delete_menu)
        self.mbtn_apply.clicked.connect(self.apply_changes)
        self.mbtn_back.clicked.connect(self.revert_changes)
        self.tblMenu.doubleClicked.connect(self.double_click_event)

        # 상태 페이지 UI 요소 초기화
        self.previous_data = []

        # 메뉴 데이터 로드
        self.load_menu_data()

    def load_menu_data(self, category=None):
        query = "SELECT menu_id, menu_name, menu_info, menu_price, category, image FROM MENU"
        
        # 조회 필터링
        menu_id = self.check_menu_id.text()
        menu_name = self.check_menu_name.text()
        menu_info = self.check_menu_info.text()
        menu_price = self.check_menu_price.text()
        category = self.check_category_combobox.currentText()
        
        filters = []
        values = []
        
        if menu_id:
            filters.append("menu_id = :1")
            values.append(menu_id)
        if menu_name:
            filters.append("menu_name LIKE :2")
            values.append(f"%{menu_name}%")
        if menu_info:
            filters.append("menu_info LIKE :3")
            values.append(f"%{menu_info}%")
        if menu_price:
            filters.append("menu_price = :4")
            values.append(menu_price)
        if category and category != '선택':
            filters.append("category = :5")
            values.append(category)

        # 필터링 조건이 있다면 쿼리에 추가
        if filters:
            query += " WHERE " + " AND ".join(filters)

        self.cursor.execute(query, tuple(values))
        
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
        # 조회 버튼 클릭 시 해당 필터링된 조건으로 조회
        self.load_menu_data()

    def add_menu(self):
        menu_name = self.menu_name_input.text()
        menu_info = self.menu_info_input.toPlainText()
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
            image_file_name = self.tblMenu.item(selected_row, 5).text()

            image_url = f"images/{image_file_name}"

            self.menu_name_input.setText(menu_name)
            self.menu_info_input.setPlainText(menu_info)
            self.menu_price_input.setText(menu_price)
            self.category_combobox.setCurrentText(category)

            self.menu_image_input.setText(image_url)

            pixmap = QPixmap(image_url)
            pixmap = pixmap.scaled(self.menu_image_input.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

            self.menu_image_input.setPixmap(pixmap)

            self.previous_data = [menu_id, menu_name, menu_info, menu_price, category, image_file_name]

    def apply_changes(self):
        reply = QMessageBox.question(self, '적용 확인', '변경 사항을 적용하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            selected_row = self.tblMenu.currentRow()
            if selected_row >= 0:
                menu_id = self.tblMenu.item(selected_row, 0).text()
                menu_name = self.tblMenu.item(selected_row, 1).text()
                menu_info = self.tblMenu.item(selected_row, 2).text()
                menu_price = self.tblMenu.item(selected_row, 3).text()
                category = self.tblMenu.item(selected_row, 4).text()
                image_url = self.tblMenu.item(selected_row, 5).text()

                self.cursor.execute(
                    """
                    UPDATE MENU
                    SET menu_name = :1, menu_info = :2, menu_price = :3, category = :4, image = :5
                    WHERE menu_id = :6
                    """, (menu_name, menu_info, menu_price, category, image_url, menu_id))

                self.conn.commit()
                self.load_menu_data()
                QMessageBox.information(self, '성공', '수정 사항이 성공적으로 적용되었습니다.')
        else:
            print("변경 사항을 적용하지 않았습니다.")

    def revert_changes(self):
        if self.previous_data:
            menu_id, menu_name, menu_info, menu_price, category, image_url = self.previous_data

            self.menu_name_input.setText(menu_name)
            self.menu_info_input.setPlainText(menu_info)
            self.menu_price_input.setText(menu_price)
            self.category_combobox.setCurrentText(category)
            self.menu_image_input.setText(image_url)

            pixmap = QPixmap(f"images/{image_url}")
            pixmap = pixmap.scaled(self.menu_image_input.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.menu_image_input.setPixmap(pixmap)

            selected_row = self.tblMenu.currentRow()
            if selected_row >= 0:
                self.tblMenu.setItem(selected_row, 0, QTableWidgetItem(menu_id))
                self.tblMenu.setItem(selected_row, 1, QTableWidgetItem(menu_name))
                self.tblMenu.setItem(selected_row, 2, QTableWidgetItem(menu_info))
                self.tblMenu.setItem(selected_row, 3, QTableWidgetItem(menu_price))
                self.tblMenu.setItem(selected_row, 4, QTableWidgetItem(category))
                self.tblMenu.setItem(selected_row, 5, QTableWidgetItem(image_url))

            print("수정 전 상태로 되돌렸습니다.")

    def closeEvent(self, event):
        if self.conn:
            self.conn.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = managerWindow()
    window.show()
    sys.exit(app.exec_())
