from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import TimeoutException 

# 1. (핵심) 여기에 수집하고 싶은 모든 상품의 URL을 리스트로 만듭니다.
product_urls = [
    "https://product.kyobobook.co.kr/detail/S000209649293", # 도쿄 디저트 여행
    "https://product.kyobobook.co.kr/detail/S000208573548", # 도쿄의 맛있는 커피집
    "https://product.kyobobook.co.kr/detail/S000000734297", # 도쿄미식회
    "https://product.kyobobook.co.kr/detail/S000001477002", # 카페도쿄
    "https://product.kyobobook.co.kr/detail/S000001609704", # 맛있는 도쿄
    "https://product.kyobobook.co.kr/detail/S000212848532", # 현지인이 다니는 진짜 도쿄 맛집을 알려줄게요 전면개정판
    "https://product.kyobobook.co.kr/detail/S000211521121", # 도쿄 카페 멋집
    "https://product.kyobobook.co.kr/detail/S000218056094", # 요즘 도쿄 맛집
    "https://product.kyobobook.co.kr/detail/S000001073279", # 고치소사마 잘 먹었습니다
    "https://product.kyobobook.co.kr/detail/S000001899596", # 동경식당
    "https://product.kyobobook.co.kr/detail/S000001556675", # 도쿄 스위트 여행
    "https://product.kyobobook.co.kr/detail/S000000734227", # 도쿄 카페 놀이
    "https://product.kyobobook.co.kr/detail/S000214758556", # 도쿄 스페셜티 커피 트립
    "https://product.kyobobook.co.kr/detail/S000216797361", # 달콤하게, 도쿄의 킷사텐
    "https://product.kyobobook.co.kr/detail/S000000510086", # 도쿄! 스토리를 찾아 떠나는 미식 산책
    "https://product.kyobobook.co.kr/detail/S000000916508", # 스위트 도쿄
    "https://product.kyobobook.co.kr/detail/S000000732418" # 도쿄 맛집 
    # ... 원하는 만큼 URL을 추가 ...
]

# 2. 드라이버 시작 
try:
    driver = webdriver.Chrome()
    print("웹 드라이버(크롬)를 성공적으로 시작합니다.")
except Exception as e:
    print(f"드라이버 시작 실패: {e}")
    exit()

# 3. URL 리스트 순회 
for url in product_urls:
    
    print("---" * 15)
    print(f"새로운 URL 처리를 시작합니다: {url}")
    print("---" * 15)
    
    try:
        driver.get(url)
        print("페이지 '맨 끝까지' 스크롤합니다...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
        print("스크롤 완료. 페이지네이션이 로드될 때까지 5초간 대기...")
        time.sleep(5) 
    except Exception as e:
        print(f"페이지 접속 또는 스크롤 중 오류 발생: {e}. 이 URL을 건너뜁니다.")
        continue 

    # 4. (★★★ XPath로 수정됨 ★★★)
    # '전체 리뷰' 탭을 찾아 클릭
    try:
        print(" -> '전체 리뷰' 탭을 찾습니다 (XPath 방식)...")
        
        # 'a' 태그가 아니어도 상관없이, "전체 리뷰" 텍스트를 포함하는
        # '모든'(*) 요소를 찾음 
        all_reviews_tab = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '전체 리뷰')]"))
        )
        
        # 강제 클릭
        driver.execute_script("arguments[0].click();", all_reviews_tab)
        print(" -> '전체 리뷰' 탭을 클릭했습니다.")
        
        # '전체 리뷰' 탭의 내용이 로드될 때까지 3초 대기
        print(" -> '전체 리뷰' 탭 로딩 대기... 3초")
        time.sleep(3)
    
    except Exception as e:
        print(f" -> [경고] '전체 리뷰' 탭을 클릭하지 못했습니다: {e}")
        print(" -> '전체 리뷰' 탭을 찾지 못했거나, 기본 탭이 이미 '전체 리뷰'일 수 있습니다.")
        print(" -> 현재 탭의 내용을 수집합니다.")
    

    # 5. 1페이지 리뷰 먼저 수집 
    print("1페이지 리뷰 수집을 시작합니다...")
    html_page_1 = driver.page_source
    soup_page_1 = BeautifulSoup(html_page_1, 'html.parser')

    review_tags_p1 = soup_page_1.find_all('div', class_='comment_text')
    current_book_reviews = [] 

    if not review_tags_p1:
        print("[경고] 1페이지에서 'div', class_='comment_text' 태그를 찾지 못했습니다.")
    else:
        for tag in review_tags_p1:
            text = tag.get_text().strip()
            if text:
                current_book_reviews.append(text)
    print(f" -> 1페이지에서 {len(current_book_reviews)}개 리뷰 수집.")

    # 6. 2페이지부터 8페이지까지 반복 클릭
    for page_num in range(2, 9): 
        try:
            print(f"'{page_num}' 페이지 버튼을 찾습니다...")
            page_button = WebDriverWait(driver, 3).until( 
                EC.element_to_be_clickable((By.LINK_TEXT, str(page_num)))
            )
            driver.execute_script("arguments[0].click();", page_button)
            print(f" -> '{page_num}' 페이지 버튼 클릭 성공.")
            time.sleep(3) 
            
            html_page = driver.page_source
            soup_page = BeautifulSoup(html_page, 'html.parser')
            review_tags = soup_page.find_all('div', class_='comment_text')
            
            new_reviews_count = 0
            for tag in review_tags:
                text = tag.get_text().strip()
                if text and (text not in current_book_reviews): 
                    current_book_reviews.append(text)
                    new_reviews_count += 1
            print(f" -> {page_num}페이지에서 {new_reviews_count}개의 새 리뷰 추가 수집.")

        except TimeoutException:
            print(f"'{page_num}' 페이지 버튼을 찾을 수 없습니다. 이 책의 수집을 마칩니다.")
            break 
        except Exception as e:
            print(f"'{page_num}' 페이지 클릭 중 오류 발생: {e}. 이 책의 수집을 마칩니다.")
            break 

    # 7. 이 책의 모든 리뷰를 'kyobo_reviews.txt'에 이어쓰기
    print(f"'{url}'의 리뷰 총 {len(current_book_reviews)}개를 파일에 저장합니다.")
    with open("kyobo_reviews.txt", "a", encoding="utf-8") as f: 
        f.write(f"\n\n### REVIEWS FROM: {url} ###\n\n") 
        for review in current_book_reviews:
            f.write(review + "\n\n") 

# 8. 모든 URL 처리가 끝난 후 드라이버 종료
driver.quit()
print("---" * 15)
print("모든 URL의 리뷰 수집이 완료되었습니다!")

