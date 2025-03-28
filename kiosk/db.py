import cx_Oracle as oci

# DB 연결 설정 변수
sid = 'XE'
host = '210.119.14.76'
# host = 'localhost'
port = 1521
username = 'kiosk'
password = '12345'

def get_db_connection():
    """
    데이터베이스 연결을 생성하는 함수
    """
    conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
    return conn

def fetch_all_menu_items():
    """
    데이터베이스에서 모든 메뉴 항목을 가져오는 함수
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = 'SELECT menu_id, menu_name, menu_info, menu_price, category, image FROM MENU'
    cursor.execute(query)

    menu_items = []
    for row in cursor:
        menu_id, menu_name, menu_info, menu_price, category, image = row
        menu_items.append({
            "menu_id": menu_id,
            "menu_name": menu_name,
            "menu_info": menu_info,
            "menu_price": menu_price,
            "category": category,
            "image": image,
        })

    cursor.close()
    conn.close()
    return menu_items