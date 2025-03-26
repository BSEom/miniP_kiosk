import requests as req
from bs4 import BeautifulSoup as bs


db_name_list = []
db_exp_list = []
db_img_list = []

url = "https://ediya.com/inc/ajax_brand.php"
params = {
    "gubun": "menu_more",
    "product_cate": "7",
    "chked_val": "",
    "skeyword": "",
    "page": 1  # 페이지 번호
}

page = 1

while True:

    print(f'{page}페이지 실행','\n')
    params["page"] = page

    # 요청 보내기
    response = req.get(url, params=params)

    # 종료 조건
    if response.status_code != 200 or "데이터 끝" in response.text or page == 23:  
        break
        
    data = response.text
    soup = bs(data, 'html.parser')
    
    
    # 메뉴 이름
    names = soup.find_all("h2")
    
    for a in range(len(names)):
        names[a] = str(names[a]).split('<span')[0].replace('<h2>', '').strip()
        db_name_list.append(names[a])
        
    # print(names, '\n')
    
    #===========================================================================

    
    # 메뉴 설명
    detail = soup.find_all("div", class_="detail_txt")
    for b in range(len(detail)):
        detail[b] = str(detail[b].text).replace('\\u200b','').replace('\\xa0', '')
        db_exp_list.append(detail[b])
    
    # print(detail, '\n')
    
    #===========================================================================
    
    
    # 이미지 링크 
    src_value = soup.find_all("img", alt="")
    src_img = [img['src'] for img in src_value]
    
    for v in range(len(src_img)):
        src_img[v] = 'https://ediya.com' + src_img[v]
        db_img_list.append(src_img[v])
        
    # print(src_img, '\n')
    
    # ===========================================================================
    page += 1


print(db_name_list, '\n')
print(db_exp_list, '\n')
print(db_img_list, '\n')