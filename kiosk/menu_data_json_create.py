import json
import cx_Oracle  # oci 사용

# DB 연결 설정

def get_db_connection():

    try:
        sid = 'XE'
        host = '210.119.14.76'
        port = 1521
        username = 'kiosk'
        password = '12345'
        return cx_Oracle.connect(f'{username}/{password}@{host}:{port}/{sid}')

    except cx_Oracle.DatabaseError as e:
        print(f"DB 연결 실패: {e}")
        return None
def fetch_data_from_db():
    conn = get_db_connection()  # oci로 연결
    if not conn:
        return []
    cursor = conn.cursor() 
    try:
        # 쿼리에서 menu_category를 category로 수정
        query = "SELECT menu_id, menu_name, menu_info, menu_price, category, image FROM menu"
        cursor.execute(query)

        # 결과 저장할 리스트
        menu_data = []

        for row in cursor.fetchall():  # fetchall로 데이터를 가져옴
            menu_data.append({
                'id': row[0],
                'name': row[1],
                'info': row[2],
                'price': row[3],
                'category': row[4],
                'image': row[5]
            })

    except cx_Oracle.DatabaseError as e:
        print(f"쿼리 실행 실패: {e}")
        menu_data = []

    finally:
        # DB 연결 종료
        cursor.close()
        conn.close()
    return menu_data

# DB에서 조회한 데이터를 JSON 파일로 저장
def save_data_to_json(menu_data):
    try:
        with open('menu_data.json', 'w', encoding='utf-8') as f:
            json.dump(menu_data, f, ensure_ascii=False, indent=4)
        print("데이터 저장 성공!")

    except Exception as e:
        print(f"데이터 저장 실패: {e}")

# 실행: DB에서 데이터 조회 후 저장
menu_data = fetch_data_from_db()
if menu_data:
    save_data_to_json(menu_data)
else:
    print("DB에서 데이터를 가져오지 못했습니다.")
