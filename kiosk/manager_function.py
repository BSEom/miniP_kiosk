import sys
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
import cx_Oracle as oci
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QTextCharFormat, QColor



# DB 연결 함수
def get_db_connection():
    sid = 'XE'
    # host = '210.119.14.76'
    host = 'localhost'
    port = 1521
    username = 'kiosk'
    password = '12345'
    return oci.connect(f'{username}/{password}@{host}:{port}/{sid}')


class managerFunction(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("ui/stats.ui", self)  # Qt Designer UI 로드
        self.initUI()

        # DB 연결
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

        self.calendar = self.findChild(QCalendarWidget, "calendar")
        self.labelStatus = self.findChild(QLabel, "labelStatus")
        self.labelStatus.setText(f"날짜를 선택해 주세요.")
        self.labelSum = self.findChild(QLabel, "labelSum")
        self.labelSum.setText(f"합계")
        
        self.start_date = None
        self.end_date = None

        # 버튼 이벤트 연결
        self.reset_btn.clicked.connect(self.reset_fn)
        self.set_btn.clicked.connect(self.update_order_data)
        self.calendar.clicked.connect(self.select_date)
        

        # 초기데이터 로드
        self.load_order_data()
        self.load_orderinfo_data()
        self.load_popular_manu()

    # 창 UI
    def initUI(self):
        self.setWindowTitle('Cafe Kiosk (관리자)')
        self.setWindowIcon(QIcon('img/coffee-cup.png'))

    def select_date(self, date):

        if self.start_date is None:
            # 첫 번째 날짜 선택
            self.start_date = date
            self.labelStatus.setText(f"시작 날짜: {date.toString('yyyy-MM-dd')}")
            self.highlight_date(date, QColor("blue"))
        elif self.end_date is None:
            # 두 번째 날짜 선택
            self.end_date = date
            self.labelStatus.setText(f"기간:  {self.start_date.toString('yyyy-MM-dd')} ~ {date.toString('yyyy-MM-dd')} 까지")
            print(self.start_date, type(self.start_date))
            print(self.end_date, type(self.end_date))

            global g_start
            g_start = self.start_date.toString('yyyy-MM-dd')
            print(g_start)
            global g_end
            g_end = self.end_date.toString('yyyy-MM-dd')
            print(g_end)
            self.highlight_range(self.start_date, self.end_date)
        else:
            # 선택 초기화
            self.reset_highlight(self, date)
            self.start_date = date
            self.end_date = None
            self.highlight_date(date, QColor("blue"))
            self.labelStatus.setText(f"시작 날짜: {date.toString('yyyy-MM-dd')}")

    # 날짜 강조
    def highlight_date(self, date, color):
        format = QTextCharFormat()
        format.setBackground(color)
        self.calendar.setDateTextFormat(date, format)

    # 날짜 범위 강조
    def highlight_range(self, start, end):
        """날짜 범위를 강조 표시"""
        if start > end:
            self.reset_highlight(self)
            self.labelStatus.setText("시작 날짜가 종료 날짜보다 늦을 수 없습니다.")
            return
        format = QTextCharFormat()
        format.setBackground(QColor("skyblue"))
        current = start
        while current <= end:
            self.calendar.setDateTextFormat(current, format)
            current = current.addDays(1)

    # 날짜 초기화
    def reset_highlight(self, *args):
        self.start_date = None
        self.end_date = None
        self.calendar.setDateTextFormat(QDate(), QTextCharFormat())
        self.labelStatus.setText(f"날짜를 선택해 주세요.")

    # 초기화 버튼 동작
    def reset_fn(self):
        self.reset_highlight(self)

        query = 'SELECT * FROM order_view'

        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        if not rows:
            print("No data found in database.")
        else:
            print(f"Fetched {len(rows)} rows from the database.")  # 데이터 확인


        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["주문번호", "주문금액", "주문날짜"])

        sum_list = []
        for row in rows:
            sum_list.append(row[1].replace(',', '').replace('원', '').strip())
            items = [QStandardItem(str(field)) for field in row]
            for index in [0, 1]: 
                items[index].setTextAlignment(Qt.AlignCenter)
            model.appendRow(items)

        ss = 0
        for s in sum_list:
            ss += int(s)
        self.labelSum.setText(f'총 매출: {ss:,}원')

        self.tableView_1.setModel(model)


    # 매출 표시
    def load_order_data(self):
        
        query = '''
        CREATE OR REPLACE VIEW order_view AS
        SELECT order_id AS id
        , to_char(order_price, '9,999,999') || '원' AS price
        , order_date AS o_date
        FROM order_table
        '''
        self.cursor.execute(query)

        query = 'SELECT * FROM order_view'

        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        if not rows:
            print("No data found in database.")
        else:
            print(f"Fetched {len(rows)} rows from the database.")  # 데이터 확인


        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["주문번호", "주문금액", "주문날짜"])
        sum_list = []
        for row in rows:
            sum_list.append(row[1].replace(',', '').replace('원', '').strip())
            items = [QStandardItem(str(field)) for field in row]
            for index in [0, 1]: 
                items[index].setTextAlignment(Qt.AlignCenter)
            model.appendRow(items)

        print(sum_list)
        # self.sum_order(self, s_list=sum_list)
        ss = 0
        for s in sum_list:
            ss += int(s)
        self.labelSum.setText(f'총 매출: {ss:,}원')
        self.tableView_1.setModel(model)

    # 기간 매출 갱신
    def update_order_data(self):
        print(g_start)
        print(g_end)

        query = '''
        SELECT * FROM order_view WHERE o_date BETWEEN to_date('
        ''' + g_start + "', 'yyyy-MM-dd') AND to_date('" +  g_end + " 23:59:59', 'yyyy-MM-dd HH24:MI:SS')"

        print(query)

        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        if not rows:
            print("No data found in database.")
        else:
            print(f"Fetched {len(rows)} rows from the database.")  # 데이터 확인


        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["주문번호", "주문금액", "주문날짜"])

        sum_list = []
        for row in rows:
            sum_list.append(row[1].replace(',', '').replace('원', '').strip())
            items = [QStandardItem(str(field)) for field in row]
            for index in [0, 1]: 
                items[index].setTextAlignment(Qt.AlignCenter)
            model.appendRow(items)

        ss = 0
        for s in sum_list:
            ss += int(s)
        self.labelSum.setText(f'총 매출: {ss:,}원')

        self.tableView_1.setModel(model)
    

    # 주문내역 표시
    def load_orderinfo_data(self):
        query = '''
        CREATE OR REPLACE VIEW orderinfo_view AS 
        SELECT i.orderinfo_id AS info_id
        , i.order_id AS o_id
        , m.menu_name	AS m_name
        , to_char(i.price, '9,999,999') || '원' AS m_price
        , i.count AS m_count
        , to_char(i.price * i.count, '9,999,999') || '원' AS m_total
        , t.order_date AS o_date
        FROM ORDERINFO i, ORDER_TABLE t, MENU m
        WHERE i.order_id = t.order_id
        AND i.menu_id = m.menu_id
        '''
        self.cursor.execute(query)

        # query = 'SELECT * FROM orderinfo_view'
        query = 'SELECT o_id, m_name, m_price, m_count, m_total, o_date FROM orderinfo_view'

        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        if not rows:
            print("No data found in database.")
        else:
            print(f"Fetched {len(rows)} rows from the database.")  # 데이터 확인


        model2 = QStandardItemModel()
        model2.setHorizontalHeaderLabels(["주문번호", "메뉴", "가격", "수량", "총액", "주문날짜"])
        for row in rows:
            items = [QStandardItem(str(field)) for field in row]
            for index in [0, 2, 3, 4]: 
                items[index].setTextAlignment(Qt.AlignCenter)
            model2.appendRow(items)

        self.tableView_2.setModel(model2)

    # 인기 항목 표시
    def load_popular_manu(self):
        query = '''
        SELECT m_name
            , sum(m_count) AS cnt
        FROM orderinfo_view
        GROUP BY m_name 
        ORDER BY cnt DESC
        '''

        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        if not rows:
            print("No data found in database.")
        else:
            print(f"Fetched {len(rows)} rows from the database.")  # 데이터 확인


        model3 = QStandardItemModel()
        model3.setHorizontalHeaderLabels(["메뉴", "총 판매수"])
        for row in rows:
            items = [QStandardItem(str(field)) for field in row]
            items[1].setTextAlignment(Qt.AlignCenter)
            model3.appendRow(items)

        self.tableView_3.setModel(model3)
        self.tableView_3.resizeColumnsToContents()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = managerFunction()
    window.show()
    sys.exit(app.exec_())




