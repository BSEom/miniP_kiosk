import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QIcon
from PyQt5 import uic

# 오류 창창
from PyQt5.QtWidgets import QMessageBox

# Oracle 모듈
import cx_Oracle as oci

# 관리자창
class managerWindow(QMainWindow, manager_form):
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

        # 버튼 시그널(이벤트) 추가
        self.mbtn_add.clicked.connect(self.mbtnAddClick)
        self.mbtn_mod.clicked.connect(self.mbtnModClick)
        self.mbtn_del.clicked.connect(self.mbtnDelClick)

        # 리스트 위젯 더블클릭 시그널 추가 (함수명 수정)
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
    def tblMenuDoubleClick(self):
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

        # 상태바에 메시지 추가 (오타 수정)
        self.statusBar().showMessage(f'{basic_msg} | 수정모드')

    # 추가버튼 클릭 시그널 처리 함수
    def mbtnAddClick(self):
        menu_id = self.input_menu_id.text()  # 메뉴 ID 가져오기
        menu_name = self.input_menu_name.text()
        menu_info = self.input_menu_info.text()
        menu_price = self.input_menu_price.text()
        menu_category = self.combo_menu_category.currentText()  # 카테고리 선택 값 가져오기

        print(menu_name, menu_info, menu_price, menu_category)

        # 입력검증 필수(Validation Check)
        if menu_name == '' or menu_price == '':
            QMessageBox.warning(self, '경고', '메뉴 이름 또는 가격은 필수입니다!')
            return  # 함수 종료

        # 이미 존재하는 메뉴라면 추가가 아니라 수정 모드
        if menu_id != '':
            QMessageBox.warning(self, '경고', '이미 존재하는 메뉴입니다. 수정 모드를 사용하세요!')
            return  # 함수 종료

        # 새 데이터 추가
        print('DB에 새 메뉴 입력 진행!')
        values = (menu_name, menu_info, menu_price, menu_category)  # 튜플로 전달

        if self.addData(values):  # 데이터베이스에 추가하는 함수 (구현 필요)
            QMessageBox.about(self, '저장 성공', '메뉴 등록 성공!!!')
        else:
            QMessageBox.about(self, '저장 실패', '관리자에게 문의하세요')

        self.loadData()  # DB에서 다시 조회하여 테이블 갱신
        self.clearInput()  # 입력 필드 초기화

    # 수정버튼 클릭 시그널 처리 함수
    def mbtnModClick(self):
        menu_id = self.input_menu_id.text()  # 메뉴 ID 가져오기
        menu_name = self.input_menu_name.text()
        menu_info = self.input_menu_info.text()
        menu_price = self.input_menu_price.text()
        menu_category = self.combo_menu_category.currentText()  # 콤보박스 선택 값

        # 메뉴 ID가 없으면 수정 불가
        if menu_id == '':
            QMessageBox.warning(self, '경고', '수정할 메뉴를 선택하세요!')
            return

        # 입력값이 없는 경우 방지
        if menu_name == '' or menu_price == '':
            QMessageBox.warning(self, '경고', '메뉴 이름 또는 가격은 필수입니다!')
            return

        # 데이터 수정 진행
        print(f'메뉴 {menu_id} 수정 진행!')
        values = (menu_name, menu_info, menu_price, menu_category, menu_id)  # 수정할 데이터

        if self.updateData(values):  # DB 업데이트 함수 (구현 필요)
            QMessageBox.about(self, '수정 성공', '메뉴 수정 성공!')
        else:
            QMessageBox.about(self, '수정 실패', '관리자에게 문의하세요')

        self.loadData()  # DB에서 다시 조회하여 테이블 갱신
        self.clearInput()  # 입력 필드 초기화


    # 삭제버튼 클릭 시그널 처리 함수
    def mbtnDelClick(self):
        menu_id = self.input_menu_id.text()  # 메뉴 ID 가져오기

        # 메뉴 ID가 없으면 삭제 불가
        if menu_id == '':
            QMessageBox.warning(self, '경고', '삭제할 메뉴를 선택하세요!')
            return

        # 사용자 확인 메시지
        reply = QMessageBox.question(self, '삭제 확인', f'정말로 메뉴 {menu_id}을(를) 삭제하시겠습니까?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            print(f'메뉴 {menu_id} 삭제 진행!')
            
            if self.deleteData(menu_id):  # DB 삭제 함수 (구현 필요)
                QMessageBox.about(self, '삭제 성공', '메뉴 삭제 성공!')
            else:
                QMessageBox.about(self, '삭제 실패', '관리자에게 문의하세요')

            self.loadData()  # DB에서 다시 조회하여 테이블 갱신
            self.clearInput()  # 입력 필드 초기화

    # 테이블위젯 데이터와 연관해서 화면 설정    
    def makeTable(self,lst_menu):
        self.tblMenu.setColumnCount(QAbstractItemView.SingleSelection) # 단일 row 선택모드
        self.tblMenu.setEditTriggers(QAbstractItemView.NoEditTriggers) #컬럼수정금지모드
        self.tblMenu.setColumnCount(4)
        self.tblMenu.setRowCount(len(lst_menu)) # 커서에 들어있는 데이터 길이만큼 row 생성
        self.tblMenu.setHorizontalHeaderLabels(['메뉴 ID','메뉴 이름', '메뉴 설명', '메뉴 가격격'])

        # 전달받은 cursor를 반복문으로 테이블위젯에 뿌리는 작업
        for i, (menu_id, menu_name, menu_info, menu_price) in enumerate(lst_menu):
            self.tblStudent.setItem(i, 0, QTableWidgetItem(str(menu_id))) # oracle number타입은 뿌릴 때 str()로 형변환 필요!
            self.tblStudent.setItem(i, 1, QTableWidgetItem(menu_name))
            self.tblStudent.setItem(i, 2, QTableWidgetItem(menu_info))
            self.tblStudent.setItem(i, 3, QTableWidgetItem(str(menu_price)))

    # R(SELECT)
    def loadData(self):
        # db연결
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        query = '''SELECT menu_id, menu_name
                      , menu_info, menu_price
                   FROM Menu'''
        cursor.execute(query)

        # for i, item in enumerate(cursor, start=1):
        #     print(item)
        lst_menu = [] # 리스트 생성
        for _, item in enumerate(cursor):
            lst_menu.append(item)

        self.makeTable(lst_menu) # 새로 생성한 리스트를 파라미터로 전달

        cursor.close()
        conn.close()

    # C(INSERT)
    def addData(self, tuples):
        isSucceed = False # 성공여부 플래그 변수
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        try:
            conn.begin() # BEGIN TRANSACTION. 트랜잭션 시작

            # 쿼리 작성
            query = '''
                    INSERT INTO kiosk.menu(STD_ID, STD_NAME, STD_MOBILE, STD_REGYEAR)
                    VALUES(SEQ_STUDENT.NEXTVAL, :v_menu_name, :v_menu_info, :v_menu_price)
                    '''
            cursor.execute(query, tuples) # query에 들어가는 동적변수 3개는 뒤의 tuples 순서대로 매핑시켜줌

            conn.commit() # DB commit 동일 기능
            last_id = cursor.lastrowid # SEQ_STUDENT.CURRVAL
            print(last_id)
            isSucceed = True # 트랜잭션 성공공
        except Exception as e:
            print(e)
            conn.rollback()  # DB rollback 동일 기능
            isSucceed = False # 트랜잭션 실패패
        finally:
            cursor.close()
            conn.close()

            # 줄 잘 맞추기!!!
            return isSucceed # 트랜잭션 여부를 리턴턴
        
        # D(DELETE)
    def delData(self, tuples):
        isSucceed = False # 성공여부 플래그 변수
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        try:
            conn.begin() # BEGIN TRANSACTION. 트랜잭션 시작

            # 쿼리 작성
            query = '''
                    DELETE FROM Students WHERE std_id = :v_std_id
                    '''
            cursor.execute(query, tuples) 

            conn.commit()
            isSucceed = True 
        except Exception as e:
            print(e)
            conn.rollback() 
            isSucceed = False
        finally:
            cursor.close()
            conn.close()

            # 줄 잘 맞추기!!!
            return isSucceed 

    # 수정 버튼 클릭 시그널 처리 함수    
    def modData(self, tuples):
        # print('수정버튼 클릭')

        isSucceed = False # 성공여부 플래그 변수
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        try:
            conn.begin() 

            
            query = '''
                    UPDATE MADANG.STUDENTS
	                   SET std_name = :v_std_name
	                     , std_mobile = :v_std_mobile
	                     , std_regyear = :v_std_regyear
                     WHERE std_id = :v_std_id
                    '''
            cursor.execute(query, tuples) 

            conn.commit() 
            last_id = cursor.lastrowid 
            print(last_id)
            isSucceed = True 
        except Exception as e:
            print(e)
            conn.rollback()  
            isSucceed = False 
        finally:
            cursor.close()
            conn.close()

            # 줄 잘 맞추기!!!
            return isSucceed 


# 실행 코드 추가
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    app.exec_()
