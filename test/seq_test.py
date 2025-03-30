import cx_Oracle

def get_all_sequences():
    try:
        # DB 연결
        conn = cx_Oracle.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        # 시퀀스 목록 조회 쿼리
        query = """
        SELECT sequence_name
        FROM user_sequences
        """
        cursor.execute(query)
        sequences = cursor.fetchall()

        if sequences:
            print("현재 사용자가 소유한 시퀀스 목록:")
            for seq in sequences:
                print(f"- {seq[0]}")
        else:
            print("현재 사용자가 소유한 시퀀스가 없습니다.")

    except cx_Oracle.DatabaseError as e:
        print(f"데이터베이스 오류: {e}")

    finally:
        cursor.close()
        conn.close()

# 시퀀스 목록 확인
if __name__ == "__main__":
    username = "kiosk"
    password = "12345"
    host = "localhost"
    port = 1521
    sid = "XE"

    get_all_sequences()
