import json
import sys
import os
import cx_Oracle as oci
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
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
        self.mbtn_check.clicked.connect(self.check_menu) 
        self.mbtn_add.clicked.connect(self.add_menu)
        self.mbtn_mod.clicked.connect(self.update_menu)
        self.mbtn_del.clicked.connect(self.delete_menu)
        self.tblMenu.doubleClicked.connect(self.double_click_event)
        self.load_menu_data() # 실행하고 조회페이지 처음엔 전체 출력해야돼서

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

    # 메뉴 존재 여부 확인(중복 등록 방지-추가버튼에서 사용함)
    def menu_exists(self, menu_name):
        query = "SELECT COUNT(*) FROM MENU WHERE menu_name = :1" 
        self.cursor.execute(query, (menu_name,)) 
        return self.cursor.fetchone()[0] > 0

    # tblMenu(조회페이지)
    def load_menu_data(self, category=None, menu_id=None, menu_name=None, menu_price=None):
        # 필터링된 데이터 준비
        filtered_data = self.menu_data

        # 카테고리 필터링
        if category and category != "선택":
            filtered_data = [menu for menu in filtered_data if menu['category'] == category]

        # 메뉴 ID 필터링
        if menu_id:
            filtered_data = [menu for menu in filtered_data if str(menu['id']) == menu_id]

        # 메뉴 이름 필터링
        if menu_name:
            filtered_data = [menu for menu in filtered_data if menu_name.lower() in menu['name'].lower()]

        # 메뉴 가격 필터링
        if menu_price:
            filtered_data = [menu for menu in filtered_data if str(menu['price']) == menu_price]

        # 테이블 컬럼 지정
        self.tblMenu.setRowCount(len(filtered_data))
        self.tblMenu.setColumnCount(7)
        self.tblMenu.setHorizontalHeaderLabels(["Status", "ID", "Name", "Info", "Price", "Category", "Image"])

        # 조회 페이지 행에 값 넣어주기
        for i in range(len(filtered_data)):
            menu = filtered_data[i]
            status = "등록됨" if self.menu_exists(menu['name']) else "등록안됨"
            self.tblMenu.setItem(i, 0, QTableWidgetItem(status))
            self.tblMenu.setItem(i, 1, QTableWidgetItem(str(menu['id'])))
            self.tblMenu.setItem(i, 2, QTableWidgetItem(menu['name']))
            self.tblMenu.setItem(i, 3, QTableWidgetItem(menu['info']))
            self.tblMenu.setItem(i, 4, QTableWidgetItem(str(menu['price'])))
            self.tblMenu.setItem(i, 5, QTableWidgetItem(menu['category']))
            self.tblMenu.setItem(i, 6, QTableWidgetItem(menu['image']))

            # 조회 페이지에선 글자 수정 불가능 상태로 만들기
            for col in range(7):  
                item = self.tblMenu.item(i, col)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

    # 조회 버튼 클릭 했을 때
    def check_menu(self):
        category = self.check_category_combobox.currentText()

        # 조회버튼 위에 입력된 값 가져오기
        menu_id = self.check_menu_id.text().strip() if self.check_menu_id.text().strip() else None
        menu_name = self.check_menu_name.text().strip() if self.check_menu_name.text().strip() else None
        menu_price = self.check_menu_price.text().strip() if self.check_menu_price.text().strip() else None

        # 필터링된 데이터 로드
        self.load_menu_data(category, menu_id, menu_name, menu_price)

    # 조회페이지에서 더블 클릭 했을 때
    def double_click_event(self):
        selected_row = self.tblMenu.currentRow()
        if selected_row >= 0:
            menu_id = self.tblMenu.item(selected_row, 1).text()
            menu_name = self.tblMenu.item(selected_row, 2).text()
            menu_info = self.tblMenu.item(selected_row, 3).text()
            menu_price = self.tblMenu.item(selected_row, 4).text()
            category = self.tblMenu.item(selected_row, 5).text()
            image_name = self.tblMenu.item(selected_row, 6).text()
            image_url = f"images/{image_name}"

            # 상태 페이지에 값 표시
            self.menu_id_input.setText(menu_id)
            self.menu_name_input.setText(menu_name)
            self.menu_info_input.setPlainText(menu_info)
            self.menu_price_input.setText(menu_price)
            self.category_combobox.setCurrentText(category)

            # label에 실제 이미지 보이도록 설정
            pixmap = QPixmap(image_url)
            pixmap = pixmap.scaled(self.menu_image_input.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.menu_image_input.setPixmap(pixmap)

            # line에 텍스트로 이미지 이름 저장(추가, 수정, 삭제 시 디비에 텍스트로 들어가야돼서)
            self.menu_image_input_name.setText(image_name)


    # 추가 버튼 클릭했을 때(상태 페이지에서 값 끌고옴)
    def add_menu(self):
        menu_id = self.menu_id_input.text()
        menu_name = self.menu_name_input.text()
        menu_info = self.menu_info_input.toPlainText()
        menu_price = self.menu_price_input.text()
        category = self.category_combobox.currentText()
        image_name = self.menu_image_input_name.text() 
        
        if menu_id and menu_name and menu_info and menu_price and category and image_name:
            if not self.menu_exists(menu_name):
                try:
                    self.cursor.execute(
                        """
                        INSERT INTO MENU (menu_id, menu_name, menu_info, menu_price, category, image)
                        VALUES (:1, :2, :3, :4, :5, :6)
                        """, (menu_id, menu_name, menu_info, menu_price, category, image_name)
                    )
                    self.conn.commit()
                    self.load_menu_data()
                    QMessageBox.information(self, "성공", "메뉴가 등록되었습니다!")
                except Exception as e:
                    print(f"오류 발생: {e}")
                    QMessageBox.critical(self, "오류", "메뉴 등록 중 오류가 발생했습니다.")
            else:
                QMessageBox.warning(self, "경고", "이 메뉴는 이미 등록되어 있습니다!")

    # 수정 버튼 클릭 했을 때(상태 페이지에서 값 가져옴)
    def update_menu(self):
        menu_id = self.menu_id_input.text() 
        menu_name = self.menu_name_input.text()
        menu_info = self.menu_info_input.toPlainText()
        menu_price = self.menu_price_input.text()
        category = self.category_combobox.currentText()
        image_name = self.menu_image_input_name.text()

        try:
            self.cursor.execute(
                """
                UPDATE MENU
                SET menu_name = :1, menu_info = :2, menu_price = :3, category = :4, image = :5
                WHERE menu_id = :6
                """, (menu_name, menu_info, menu_price, category, image_name, menu_id)) 
            self.conn.commit()
            self.load_menu_data()
            QMessageBox.information(self, "성공", "수정 성공!")
        except Exception as e:
            print(f"오류 발생: {e}")
            QMessageBox.critical(self, "오류", "수정 중 오류가 발생했습니다!")

    # 삭제 버튼 클릭했을 때(상태 페이지에서 값 가져옴)
    def delete_menu(self):
        menu_name = self.menu_name_input.text()
        if menu_name:
            try:
                self.cursor.execute("DELETE FROM MENU WHERE menu_name = :1", (menu_name,))
                self.conn.commit()
                self.load_menu_data()
                QMessageBox.information(self, "성공", "삭제 성공!")
            except Exception as e:
                print(f"오류 발생: {e}")
                QMessageBox.critical(self, "오류","삭제 중 오류가 발생했습니다!")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ManagerWindow()
    window.show()
    sys.exit(app.exec_())
