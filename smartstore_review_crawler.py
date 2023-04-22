from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import os

# 스마트 스토어 url
url = "https://smartstore.naver.com/echungwoo/products/"
# 리뷰를 가져오려는 제품번호
product_no = '4486426425'

# 새로운 폴더를 생성한다.
folder_path = product_no

# 생성된 폴더가 존재하는지 확인한다.
if os.path.exists(folder_path):
    print(f'{folder_path} 폴더가 이미 생성되어 있습니다.')
else:
    os.makedirs(folder_path)
    print(f'{folder_path} 폴더를 생성하였습니다.')

# Chrome 브라우저 옵션 설정
chrome_options = Options()
chrome_options.add_argument('--headless')  # 브라우저 창 숨기기

# Chrome 웹 드라이버 실행
driver = webdriver.Chrome(options=chrome_options)
driver.get(f'{url}{product_no}')

# 3초 뒤 하위 코드 실행
time.sleep(3)

# 스토어 픽 리뷰 탭 열기
review_tabs = driver.find_elements(By.CLASS_NAME, '_1ykMw2f75V')
review_tabs[2].click()

# 3초 뒤 하위 코드 실행
time.sleep(3)

# store pick reviews
store_pick_reviews_HTML = driver.execute_script('return document.querySelector("._2389dRohZq").parentElement.innerHTML')

# 드라이버 종료
driver.quit()

# BeautifulSoup 객체 생성
soup = BeautifulSoup(store_pick_reviews_HTML, 'html.parser')

review_items = soup.find_all('li', {"class": "_2389dRohZq"})

i = 0
for review_item in review_items:
  i = i + 1

  soup_reivew_item = BeautifulSoup(str(review_item), 'html.parser')

  # 별점
  review_stars_dom = soup_reivew_item.select_one('._2V6vMO_iLm em._15NU42F3kT')
  if review_stars_dom is not None :
    review_stars = review_stars_dom.text
  else :
    review_stars = 'No Stars'
  print('별점을 가져왔습니다.')

  # 작성자
  review_writer_dom = soup_reivew_item.select_one('._2FmJXrTVEX strong._3QDEeS6NLn')
  if review_writer_dom is not None :
    review_writer = review_writer_dom.text
  else :
    review_writer = 'No Writer'
  print('작성자를 가져왔습니다.')

  # 작성일자
  review_date_dom = soup_reivew_item.select_one('._2FmJXrTVEX span._3QDEeS6NLn')
  if review_date_dom is not None :
    review_date = review_date_dom.text
  else :
    review_date = 'No Date'
  print('작성일자를 가져왔습니다.')

  # 리뷰내용
  review_content_dom = soup_reivew_item.select_one('._19SE1Dnqkf span._3QDEeS6NLn')
  if review_content_dom is not None :
    review_content = review_content_dom.text
  else :
    review_content = 'No Content'
  print('리뷰내용을 가져왔습니다.')

  # 리뷰 이미지
  review_img_dom = soup_reivew_item.select('img')
  if review_img_dom is not None :
    review_img = review_img_dom[1]['src']
  else :
    review_img = 'No Img'
  print('리뷰 이미지를 가져왔습니다.')

  # 결과물 정리
  result_str = '{'
  result_str += f'''
  "review_stars": "{str(review_stars)}",
  "review_writer": "{str(review_writer)}",
  "review_date": "{str(review_date)}",
  "review_content": "{str(review_content)}",
  "review_img": "{str(review_img).split('?')[0]}",
'''
  result_str += '}'

  # 텍스트 파일로 결과 내보내기
  with open(f'{folder_path}/review_{i}.txt', 'w', encoding='utf-8') as f:
    f.write(str(result_str))



