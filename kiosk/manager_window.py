import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QIcon
from PyQt5 import uic

# Oracle 모듈
import cx_Oracle as oci

## DB 연결 설정
sid = 'XE'
host = '210.119.14.76' 
port = 1521
username = 'kiosk' 
password = '12345'
basic_msg = '학생정보 v1.0'

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        self.loadData()

    def initUI(self):
        uic.loadUi(r'./ui/manager.ui', self)  # UI 파일 로드
        self.setWindowTitle('학생정보앱')
        self.setWindowIcon(QIcon('./image/duck.png'))

        # 상태바 메시지 추가
        self.statusBar().showMessage('관리자모드')

        # 버튼 시그널(이벤트) 추가 (하나의 함수로 처리)
        self.mbtn_add.clicked.connect(self.mbtnAddClick)
        self.mbtn_mod.clicked.connect(self.mbtnModClick)
        self.mbtn_del.clicked.connect(self.mbtnDelClick)

        # 리스트 위젯 더블클릭 시그널 추가
        self.tblMenu.itemDoubleClicked.connect(self.tblMenuDoubleClick)

        self.show()

    # 화면의 인풋위젯 데이터 초기화함수
    def clearInput(self):
        self.input_menu_id.clear()
        self.input_menu_name.clear()
        self.input_menu_info.clear()
        self.input_menu_price.clear()
        self.combo_menu_category.setCurrentIndex(0)

    # 테이블 위젯 더블클릭 시그널 처리 함수
def tblStudentDoubleClick(self):
    selected = self.tblMenu.currentRow()  # 현재 선택된 행의 인덱스 가져오기
    
    # 선택된 셀의 값 가져오기
    menu_id = self.tblMenu.item(selected, 0).text()
    menu_name = self.tblMenu.item(selected, 1).text()
    menu_info = self.tblMenu.item(selected, 2).text()
    menu_price = self.tblMenu.item(selected, 3).text()
    menu_category = self.tblMenu.item(selected, 4).text()  # 크롤링한 데이터에서 가져온 카테고리

    # 가져온 데이터를 입력창에 반영
    self.input_menu_id.setText(menu_id)
    self.input_menu_name.setText(menu_name)
    self.input_menu_info.setText(menu_info)
    self.input_menu_price.setText(menu_price)

    # ✅ 크롤링된 카테고리가 QComboBox에 있으면 설정
    categories = [self.combo_menu_category.itemText(i) for i in range(self.combo_menu_category.count())]

    if menu_category in categories:
        self.combo_menu_category.setCurrentText(menu_category)
    else:
        print(f"⚠ '{menu_category}' 값이 콤보박스에 없음! 기본값으로 설정")
        self.combo_menu_category.setCurrentIndex(0)  # 기본값으로 설정
  

        # 상태바에 메시지 추가
        self.statusbar.showMessage(f'{basic_msg} | 수정모드')

    # 추가버튼 클릭 시그널처리 함수
    def mbtnAddClick(self):
        # print('추가버튼 클릭')
        std_id = self.input_std_id.text()
        std_name = self.input_std_name.text()   # 밑에 있는 std_name이랑은 다른거임
        std_mobile = self.input_std_mobile.text()
        std_regyear = self.input_std_regyear.text()
        print(std_name, std_mobile, std_regyear)



# 실행 코드 추가
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    app.exec_()



