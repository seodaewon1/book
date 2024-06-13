from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
filename = f"Kyobo/Geonseol/Geonseol_{current_date}.json"


# 웹드라이버 설치
options = ChromeOptions() 
options.add_argument("--start-maximized") 
options.add_argument("--headless")  # Headless 모드 추가
options.add_argument("--no-sandbox")  # Sandbox 모드 비활성화
options.add_argument("--disable-dev-shm-usage")  # /dev/shm 사용 비활성화
options.add_argument("--disable-gpu")  # GPU 비활성화
options.add_argument("--window-size=1920x1080")  # 윈도우 크기 설정
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)

# URL 열기
browser.get('https://search.kyobobook.co.kr/search?keyword=%EA%B1%B4%EC%84%A4%20%EC%95%88%EC%A0%84%20%EA%B8%B0%EC%82%AC&target=total&gbCode=TOT&len=30')

# 페이지가 완전히 로드될 때까지 대기
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "result_area"))
)

# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')

# 데이터 추출
book_data = []

# 첫 번째 tracks
tracks = soup.select(".prod_list .prod_item")

for track in tracks:
    spans = track.select(".auto_overflow_inner span")
    if len(spans) >= 2:  # 두 번째 span 요소가 있는지 확인
        title = spans[1].text.strip()
        author = track.select_one(".auto_overflow_inner a.author.rep").text.strip()
        price = track.select_one(".price span").text.strip()
        # 이미지 요소가 로드될 때까지 대기
        image_element = track.select_one(".img_box .prod_img_load")  # 이미지 요소 가져오기
        image_url = image_element.get('src') if image_element else None  # src에서 이미지 URL 가져오기
        link_element = track.select_one(".auto_overflow_inner a")  # 링크 요소 가져오기
        href = link_element.get('href') if link_element else None  # href 속성 가져오기


        book_data.append({
            "title": title,
            "imageURL": image_url,
            "author": author,
            "price" : price,
            "url" : href
        })

print(book_data)

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(book_data, f, ensure_ascii=False, indent=4)

# 브라우저 종료
browser.quit()
