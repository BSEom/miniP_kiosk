import cx_Oracle as oci

# DB연결 설정변수 선언
sid = 'XE'
host = '210.119.14.76' 
port = 1521
username = 'kiosk' 
password = '12345'

# DB 연결 시작
conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
cursor = conn.cursor() 

# 읽어오기
query = 'SELECT menu_id, menu_name, menu_info, menu_price, category, image FROM MENU' 
cursor.execute(query)

# 불러온 데이터 처리
for i, row in enumerate(cursor, start=1):
    menu_id, menu_name, menu_info, menu_price, category, image = row
    
    # 각 컬럼을 따로 변수로 사용
    print(f"메뉴ID: {menu_id}")
    print(f"메뉴명: {menu_name}")
    print(f"메뉴설명: {menu_info}")
    print(f"가격: {menu_price}")
    print(f"카테고리: {category}")
    print(f"이미지경로(또는 URL): {image}")
    print("-" * 40)  # 구분선

cursor.close()
conn.close()
