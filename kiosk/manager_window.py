import json
import sys
import os
import shutil
import cx_Oracle as oci
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from manager_function import managerFunction

class managerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ui/manager.ui", self)  # UI 로드
        self.initUI()

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
        self.stats_btn.clicked.connect(self.managerFunction)
        self.load_menu_data() # 조회페이지

    # 디비 연결
    def get_db_connection(self):
        sid = 'XE'
        host = 'localhost'
        port = 1521
        username = 'kiosk'
        password = '12345'
        return oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
    
    # 상태바 이름, Icon
    def initUI(self):
        self.setWindowTitle('Cafe Kiosk (관리자)')
        self.setWindowIcon(QIcon('img/coffee-cup.png'))

    # menu_data.json 파일 끌고오기
    def load_json_data(self):
        try:
            with open('kiosk/menu_data.json', 'r', encoding='utf-8') as f:  
                return json.load(f) 
        except (FileNotFoundError, json.JSONDecodeError):
            QMessageBox.critical(self, "오류", "JSON 파일이 손상되었거나 존재하지 않습니다. 프로그램을 종료합니다.")
            sys.exit()
        
    # 메뉴 이름, 아이디 존재 여부 확인(중복 등록 방지)
    def menu_exists(self, menu_name, menu_id=None):
        # 메뉴 이름과 아이디가 모두 중복되는지 확인
        query = "SELECT COUNT(*) FROM MENU WHERE menu_name = :1 OR menu_id = :2"
        self.cursor.execute(query, (menu_name, menu_id)) 
        return self.cursor.fetchone()[0] > 0  # 중복 있으면 True 반환

    # tblMenu(조회페이지)
    def load_menu_data(self, category=None, menu_id=None, menu_name=None, menu_price=None):
        # 필터링된 데이터 준비
        filtered_data = self.menu_data

        # 필터링
        if category and category != "선택":
            filtered_data = [menu for menu in filtered_data if menu['category'] == category]
        if menu_id:
            filtered_data = [menu for menu in filtered_data if str(menu['id']) == menu_id]
        if menu_name:
            filtered_data = [menu for menu in filtered_data if menu_name.lower() in menu['name'].lower()]
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

    # JSON 파일 읽기
    def read_json_file(self):
        try:
            with open('kiosk/menu_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"JSON 파일 읽기 중 오류 발생: {e}")
            return []

    # JSON 파일 쓰기
    def write_json_file(self, menu_data):
        try:
            with open('kiosk/menu_data.json', 'w', encoding='utf-8') as f:
                json.dump(menu_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"JSON 파일 쓰기 중 오류 발생: {e}")

    # 메뉴 추가
    def add_to_json(self, new_menu):
        menu_data = self.read_json_file()

        if not any(menu['name'] == new_menu['name'] for menu in menu_data):
            menu_data.append(new_menu)
            self.write_json_file(menu_data)
            self.menu_data = menu_data


    # 추가 버튼 클릭했을 때(상태 페이지에서 값 끌고옴)
    def add_menu(self):
        menu_id = self.menu_id_input.text()
        menu_name = self.menu_name_input.text()
        menu_info = self.menu_info_input.toPlainText()
        menu_price = self.menu_price_input.text()
        category = self.category_combobox.currentText()
        image_name = self.menu_image_input_name.text()
        
        if not all([menu_id, menu_name, menu_info, menu_price, category, image_name]):
            QMessageBox.warning(self, "입력 오류", "⭐ 부분은 필수항목입니다. 모두 입력해주세요.")
            return
        
        # 중복 체크 추가
        if self.menu_exists(menu_name, menu_id):
            QMessageBox.warning(self, "중복 오류", f"아이디 {menu_id} 또는 메뉴명 {menu_name}은 이미 존재합니다!")
            return

        # 메뉴 정보 딕셔너리로 구성
        new_menu = {
            'id' : menu_id,
            'name': menu_name,
            'info': menu_info,
            'price': menu_price,
            'category': category,
            'image': image_name
        }
        try:
            # JSON에 새로운 메뉴 추가
            self.add_to_json(new_menu)

            query = """
            INSERT INTO MENU (menu_id, menu_name, menu_info, menu_price, category, image)
            VALUES (:1, :2, :3, :4, :5, :6)
            """
            self.cursor.execute(query, (menu_id, menu_name, menu_info, menu_price, category, image_name))
            self.conn.commit()

            # 추가 후 값 클리어
            self.clear_inputs()

            QMessageBox.information(self, "성공", "추가 성공!")
        except Exception as e:
            print(f"오류 발생: {e}")
            QMessageBox.critical(self, "오류", f"추가 중 오류가 발생했습니다: {e}")

        self.load_menu_data()

    # 메뉴 수정
    def update_json(self, menu_id, menu_name, menu_info, menu_price, category, image_name):
        menu_data = self.read_json_file()
        found = False

        for menu in menu_data:
            if menu['name'] == menu_name:  # menu_name 기준으로 검색
                menu['id'] = int(menu_id)
                menu['name'] = menu_name
                menu['info'] = menu_info
                menu['price'] = int(menu_price)  # 숫자 형태 유지
                menu['category'] = category
                menu['image'] = image_name
                found = True
                break  # 수정 후 반복문 종료

        if found:
            self.write_json_file(menu_data)
        else:
            return False  # 메뉴를 찾지 못했을 때 False 반환

    # 수정 버튼 클릭했을 때(상태 페이지에서 값 가져옴)
    def update_menu(self):
        selected_row = self.tblMenu.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "선택오류", "조회페이지에서 수정할 메뉴를 먼저 선택해주세요")
            return
        
        # 상태 페이지에서 가져온 값
        menu_id = self.menu_id_input.text() 
        menu_name = self.menu_name_input.text()
        menu_info = self.menu_info_input.toPlainText()
        menu_price = self.menu_price_input.text()
        category = self.category_combobox.currentText()
        image_name = self.menu_image_input_name.text()

        # 메뉴명으로 찾기
        current_menu_name = self.tblMenu.item(selected_row, 2).text()

        if menu_name != current_menu_name:
            QMessageBox.warning(self, "수정 불가", "메뉴명은 수정할 수 없습니다.")
            return

        if not all([menu_id, menu_name, menu_info, menu_price, category, image_name]):
            QMessageBox.warning(self, "입력 오류", "⭐ 부분은 필수항목입니다. 모두 입력해주세요.")
            return
        
        # JSON에서 해당 menu_name 찾기
        if not self.update_json(menu_id, menu_name, menu_info, menu_price, category, image_name):
            QMessageBox.warning(self, "수정 오류", "조회페이지에 없는 음료입니다.\n새로운 메뉴는 추가 버튼을 눌려주세요.")
            return

        try:
            # JSON에 등록된 기존 메뉴 수정
            self.update_json(menu_id, menu_name, menu_info, menu_price, category, image_name)

            # DB 수정
            query = """
            UPDATE MENU
            SET menu_name = :1, menu_info = :2, menu_price = :3, category = :4, image = :5
            WHERE menu_name = :6  # 메뉴명 기준으로 수정
            """
            self.cursor.execute(query, (menu_name, menu_info, menu_price, category, image_name, menu_name))
            self.conn.commit()

            # 수정 후, UI 업데이트
            self.clear_inputs()

            self.load_menu_data()

            QMessageBox.information(self, "성공", "수정 성공!")
        except Exception as e:
            print(f"오류 발생: {e}")
            QMessageBox.critical(self, "오류", f"수정 중 오류가 발생했습니다: {e}")



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
                QMessageBox.critical(self, "오류",f"삭제 중 오류가 발생했습니다:{e}")
            
            self.clear_inputs()

    def clear_inputs(self):
        self.menu_id_input.clear()
        self.menu_name_input.clear()
        self.menu_info_input.clear()
        self.menu_price_input.clear()
        self.menu_image_input_name.clear()
        self.menu_image_input.clear()

    def managerFunction(self):
        self.window_5 = managerFunction()
        self.window_5.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = managerWindow()
    window.show()
    sys.exit(app.exec_())
