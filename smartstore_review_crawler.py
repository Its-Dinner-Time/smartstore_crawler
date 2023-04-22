## Chat gpt로 개선한 사항들

## 1.
# - time 모듈을 사용하여 프로그램 실행을 지연시키는 부분이 있는데, 
# - 이 부분은 리뷰 탭이 로딩될 때까지 대기하는 용도로 사용하고 있습니다. 
# - 이 부분을 조금 더 효율적으로 개선하려면, 
# - WebDriverWait 클래스를 사용하여 리뷰 탭이 로딩될 때까지 
# - 대기하는 코드로 변경하는 것이 좋습니다.

## 2.
# - driver.execute_script() 메서드를 사용하여 
# - 스토어 픽 리뷰 HTML을 가져오고 있습니다. 
# - 이 부분은 BeautifulSoup으로도 해결 가능합니다. 
# - soup.select() 메서드를 사용하여 선택자를 지정하면, 
# - 해당 선택자에 해당하는 HTML 코드를 추출할 수 있습니다.

## 3.
# 각 리뷰의 데이터를 파일로 저장하는 부분은 크게 문제가 없어 보입니다. 
# 하지만, JSON 형식으로 데이터를 저장하는 것이 좀 더 구조적으로 좋을 수 있습니다. 
# 이 경우, json 모듈을 사용하여 데이터를 JSON 형식으로 저장할 수 있습니다.

## 4.
# enumerate() 함수를 사용하여 반복문을 수행하고, 
# review_data라는 딕셔너리 객체를 만들어서 데이터를 저장하도록 변경하였습니다.

## 5.
# 마지막으로, soup.select() 메서드를 사용하여 
# 선택자를 지정하여 리뷰 데이터를 추출하고 있습니다. 
# 이를 통해 코드의 가독성을 높이고, 복잡한 선택자도 쉽게 지정할 수 있습니다.

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import json
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def crawler(shop: str, product_no: str):
  # 스마트 스토어 URL
  url = f'https://smartstore.naver.com/{shop}/products/'

  # 새로운 폴더를 생성한다.
  folder_path = f'{shop}'

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

  # 리뷰 탭을 찾을 때까지 대기
  wait = WebDriverWait(driver, 10)
  review_tabs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, '_1ykMw2f75V')))
  review_tabs[2].click()

  # 스토어 픽 리뷰 HTML을 추출
  soup = BeautifulSoup(driver.page_source, 'html.parser')
  review_items = soup.select('._2389dRohZq')

  result_data = []

  for i, review_item in enumerate(review_items, start=1):
      soup_review_item = BeautifulSoup(str(review_item), 'html.parser')
      review_data = {}

      # 별점
      review_stars_dom = soup_review_item.select_one('._2V6vMO_iLm em._15NU42F3kT')
      if review_stars_dom is not None:
        review_stars = review_stars_dom.text
      else:
          review_stars = 'No Stars'

      # 작성자
      review_writer_dom = soup_review_item.select_one('._2FmJXrTVEX strong._3QDEeS6NLn')
      if review_writer_dom is not None:
          review_writer = review_writer_dom.text
      else:
          review_writer = 'No Writer'

      # 작성일자
      review_date_dom = soup_review_item.select_one('._2FmJXrTVEX span._3QDEeS6NLn')
      if review_date_dom is not None:
          review_date = review_date_dom.text
      else:
          review_date = 'No Date'

      # 리뷰내용
      review_content_dom = soup_review_item.select_one('._19SE1Dnqkf span._3QDEeS6NLn')
      if review_content_dom is not None:
          review_content = review_content_dom.text
      else:
          review_content = 'No Content'

      # 리뷰 이미지
      review_img_dom = soup_review_item.select('img')
      if review_img_dom is not None and len(review_img_dom) > 1:
          review_img = review_img_dom[1]['src']
      else:
          review_img = 'No Img'

      # 결과물 정리
      review_data['review_id'] = i
      review_data['review_stars'] = review_stars
      review_data['review_writer'] = review_writer
      review_data['review_date'] = review_date
      review_data['review_content'] = review_content
      review_data['review_img'] = str(review_img).split('?')[0]

      result_data.append(review_data)

   
  # JSON 파일로 결과 내보내기
  with open(f'{folder_path}/{product_no}.json', 'w', encoding='utf-8') as f:
    json.dump(result_data, f, ensure_ascii=False)

  # 드라이버 종료
  driver.quit()