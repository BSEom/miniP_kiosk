import cx_Oracle as oci
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtGui, uic

# DB연결 설정변수 선언
sid = 'XE'
host = '210.119.14.76'
port = 1521 
username = 'kiosk'
password = '12345'

conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
cursor = conn.cursor() 

query = 'SELECT * FROM menu'
cursor.execute(query)

# 불러온 데이터 처리
for i, (menu_id, menu_name, exp, menu_price, category, image) in enumerate(cursor, start=1):
    print(menu_id, menu_name, exp, menu_price, category, image)

cursor.close()
conn.close()

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#         self.initUI()
#         self.loadData()

#     def initUI(self):
#         uic.loadUi('', self)
#         self.setWindowTitle('카페 키오스크')

#         self.show()

#     def loadData(self):
#         # DB연결
#         conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
#         cursor = conn.cursor()

#         query = 'SELECT * FROM menu'
#         cursor.execute(query)

#         # 불러온 데이터 처리
#         for i, (menu_id, menu_name, exp, menu_price, category, image) in enumerate(cursor, start=1):
#             print(menu_id, menu_name, exp, menu_price, category, image)

#         cursor.close()
#         conn.close()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     win = MainWindow()
#     app.exec_()
