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
        self.input_std_name.clear()
        self.input_std_mobile.clear()
        self.input_std_regyear.clear()

    # 테이블 위젯 더블클릭 시그널 처리 함수
    def tblStudentDoubleClick(self):
        selected = self.tblStudent.currentRow() # 현재 선택된 row값을 반환하는 함수
        std_id = self.tblStudent.item(selected, 0).text()
        std_name = self.tblStudent.item(selected, 1).text()
        std_mobile = self.tblStudent.item(selected, 2).text()
        std_regyear = self.tblStudent.item(selected, 3).text()
        # QMessageBox.about(self,'더블클릭',f'{std_id}, {std_name}, {std_mobile}, {std_regyear}')  
        # 더블클릭하면 학생정보 입력창에 올라감
        self.input_std_id.setText(std_id)
        self.input_std_name.setText(std_name)
        self.input_std_mobile.setText(std_mobile)
        self.input_std_regyear.setText(std_regyear)  

        # 상태바에 메시지 추가
        self.statusbar.showMessage(f'{basic_msg} | 수정모드')

# 실행 코드 추가
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    app.exec_()



