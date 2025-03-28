import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog, QTextEdit, QMessageBox, QLineEdit, QComboBox, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
import cx_Oracle as oci
from PyQt5.QtCore import Qt
import os
import random as r
import requests as req
from bs4 import BeautifulSoup as bs

# DB 연결 함수
def get_db_connection():
    sid = 'XE'
    host = '210.119.14.76'
    port = 1521
    username = 'kiosk'
    password = '12345'
    return oci.connect(f'{username}/{password}@{host}:{port}/{sid}')

# 크롤링한 데이터를 저장할 리스트
save_folder = "images"
os.makedirs(save_folder, exist_ok=True)

db_name_list = []
db_exp_list = []
db_img_list = []
db_categori_list = []
db_price_list = []

# 카테고리 리스트
cate_list = ['12,', '13,', '14,', '15,', '16,']
cate = ''

url = "https://ediya.com/inc/ajax_brand.php"
params = {
    "gubun": "menu_more",
    "product_cate": "7",
    "chked_val": "12,",  # 카테고리
    "skeyword": "",
    "page": 1  # 페이지 번호
}

# 크롤링 함수
def crawl_data():
    global db_name_list, db_exp_list, db_img_list, db_categori_list, db_price_list
    for c in cate_list:
        if c == cate_list[0]:
            cate = '커피'
        elif c == cate_list[1]:
            cate = '음료'
        elif c == cate_list[2]:
            cate = '차'
        elif c == cate_list[3]:
            cate = '플렛치노'
        elif c == cate_list[4]:
            cate = '쉐이크&에이드'
        else:
            cate = 'none'

        page = 1

        while True:
            params["page"] = page
            params["chked_val"] = c
            response = req.get(url, params=params)

            # 종료 조건
            if response.status_code != 200 or response.text == 'none':  
                break

            data = response.text
            soup = bs(data, 'html.parser')

            # 메뉴 이름
            names = soup.find_all("h2")
            for a in range(len(names)):
                names[a] = str(names[a]).split('<span')[0].replace('<h2>', '').strip()
                db_name_list.append(names[a])
                db_categori_list.append(cate)
                db_price_list.append(r.randrange(4000, 6500, 100))

            # 메뉴 설명
            detail = soup.find_all("div", class_="detail_txt")
            for b in range(len(detail)):
                detail[b] = str(detail[b].text).replace('\u200b','').replace('\xa0', '').replace('\r\n', '')
                db_exp_list.append(detail[b])

            # 이미지 링크 
            src_value = soup.find_all("img", alt="")
            src_img = [img['src'] for img in src_value]
            for v in range(len(src_img)):
                img_url = src_img[v].replace('/files/menu/', '')
                src_img[v] = 'https://ediya.com' + src_img[v]
                db_img_list.append(img_url)

                img_data = req.get(src_img[v]).content
                img_name = os.path.join(save_folder, os.path.basename(img_url))
                with open(img_name, "wb") as img_file:
                    img_file.write(img_data)

            page += 1

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
        self.mbtn_apply.clicked.connect(self.apply_changes)
        self.mbtn_back.clicked.connect(self.revert_changes)
        self.tblMenu.doubleClicked.connect(self.double_click_event)

        # 상태 페이지 UI 요소 초기화
        self.previous_data = []

        # 크롤링 데이터 로드
        crawl_data()

        # 메뉴 데이터 로드
        self.load_menu_data()

    def load_menu_data(self):
        query = "SELECT menu_id, menu_name, menu_info, menu_price, category, image FROM MENU"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # 테이블 설정
        self.tblMenu.setRowCount(len(db_name_list))
        self.tblMenu.setColumnCount(7)
        self.tblMenu.setHorizontalHeaderLabels(["ID", "Name", "Info", "Price", "Category", "Image", "Status"])

        for i, name in enumerate(db_name_list):
            menu_id = f"{i+1}"
            menu_name = db_name_list[i]
            menu_info = db_exp_list[i]
            menu_price = db_price_list[i]
            category = db_categori_list[i]
            image_url = db_img_list[i]

            # DB에 존재하는지 확인
            status = "등록됨" if menu_name in [row[1] for row in rows] else "등록안됨"

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
            self.load_menu_data()

    def revert_changes(self):
        # 수정 전 상태로 되돌리기
        self.menu_name_input.setText(self.previous_data[1])
        self.menu_info_input.setPlainText(self.previous_data[2])
        self.menu_price_input.setText(self.previous_data[3])
        self.category_combobox.setCurrentText(self.previous_data[4])
        self.menu_image_input.setText(self.previous_data[5])

        # 이미지 파일 경로 업데이트
        image_url = f"images/{self.previous_data[5]}"
        pixmap = QPixmap(image_url)
        pixmap = pixmap.scaled(self.menu_image_input.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.menu_image_input.setPixmap(pixmap)

        print("수정 전 상태로 되돌렸습니다.")

    def closeEvent(self, event):
        # 창을 닫을 때 DB 연결 종료
        if self.conn:
            self.conn.close()
        event.accept()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = managerWindow()
    window.show()
    sys.exit(app.exec_())
