import os
import random as r
import requests as req
from bs4 import BeautifulSoup as bs
import cx_Oracle as oci
# import oracledb as oci

# DB연결 설정변수 선언
sid = 'XE'
host = 'localhost'  # localhost와 동일한 의미.
# DB 서버가 외부에 있다면 oracle.pkunqrd.net(호스트가 포함된 도메인 주소) 또는 211.12.11.45(ip 주소)로 입력 필요
port = 1521
username = 'kiosk' # madang dbeaver에서 만듦
password = '12345'

# DB 연결 시작
conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
cursor = conn.cursor() # DB 커서와 동일한 역할을 하는 개체


save_folder = "images"
os.makedirs(save_folder, exist_ok=True)

db_name_list = []
db_exp_list = []
db_img_list = []
db_categori_list = []
db_price_list = []

# 12 = 커피, 13 = 음료, 14 = 차, 15 = 플렛치노, 16 = 쉐이크&에이드
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
        
        print(f'{page}페이지 실행','\n')
        
        params["page"] = page
        params["chked_val"] = c
        print(params["chked_val"])
        # prepared_request = req.Request('GET', url, params=params).prepare()
        # print(prepared_request.url)
        
        # 요청 보내기
        response = req.get(url, params=params)
        
        # 종료 조건
        if response.status_code != 200 or response.text == 'none':  
            print('멈춤', '\n')
            break
            
        data = response.text
        soup = bs(data, 'html.parser')
        # print(data, '\n')
        
        # 메뉴 이름
        names = soup.find_all("h2")
        
        
        for a in range(len(names)):
            names[a] = str(names[a]).split('<span')[0].replace('<h2>', '').strip()
            db_name_list.append(names[a])
            db_categori_list.append(cate)
            db_price_list.append(r.randrange(4000,6500,100))

            
            
        # print(names, '\n')
        
        #===========================================================================
    
        
        # 메뉴 설명
        detail = soup.find_all("div", class_="detail_txt")
        for b in range(len(detail)):
            detail[b] = str(detail[b].text).replace('\u200b','').replace('\xa0', '').replace('\r\n', '')
            db_exp_list.append(detail[b])
        
        # print(detail, '\n')
        
        #===========================================================================
        
        
        # 이미지 링크 
        src_value = soup.find_all("img", alt="")
        src_img = [img['src'] for img in src_value]
        
        for v in range(len(src_img)):
            img_url = src_img[v].replace('/files/menu/','')
            src_img[v] = 'https://ediya.com' + src_img[v]
            db_img_list.append(img_url)

            img_data = req.get(src_img[v]).content
            img_name = os.path.join(save_folder, os.path.basename(img_url))
            with open(img_name, "wb") as img_file:
                img_file.write(img_data)
            print(f"Downloaded: {img_name}")

            
        # print(src_img, '\n')
        
        # ===========================================================================
        page += 1


print(db_name_list, '\n')
print(db_exp_list, '\n')
print(db_img_list, '\n')
print(db_categori_list, '\n')
print(db_price_list, '\n')


# ✅ DB 저장을 위한 데이터 준비
menu_data = []
cursor.execute("SELECT NVL(MAX(menu_id), 0) + 1 FROM MENU")  # 현재 최대 ID 가져오기
menu_id_start = cursor.fetchone()[0]

for i in range(len(db_name_list)):
    menu_data.append((menu_id_start + i, db_name_list[i], db_exp_list[i], db_price_list[i], db_categori_list[i], db_img_list[i]))  # 가격은 NULL 처리

# 🔹 INSERT SQL 실행
insert_query = """
    INSERT INTO MENU (menu_id, menu_name, menu_info, menu_price, category, image)
    VALUES (:1, :2, :3, :4, :5, :6)
"""
cursor.executemany(insert_query, menu_data)

# 🔹 커밋 후 종료
conn.commit()
cursor.close()
conn.close()

print("✅ 데이터 저장 완료!")


# DB 연결 시작
conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
cursor = conn.cursor() # DB 커서와 동일한 역할을 하는 개체

# 읽어오기
query = 'SELECT * FROM MENU' # 파이썬에서 쿼리호출할 때 ; 삭제하고 넣기(넣으면 오류남)
cursor.execute(query)

# 불러온 데이터 처리
for i, (menu_id,menu_name, exp, menu_price, category, image) in enumerate(cursor, start=1):
    print(menu_id,menu_name, exp, menu_price, category, image)
   
cursor.close()
conn.close()
# DB는 연결하면 마지막에 close() 해주기, 파일은 오픈하면 마지막에 닫아줘야 됨