from konlpy.tag import Okt
from collections import Counter

# 0. konlpy (Okt) 설치가 필요합니다.
# pip install konlpy

# 1. 수집한 텍스트 파일 읽기
with open("kyobo_reviews.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 2. Okt 객체 생성
okt = Okt()

# 3. 명사(Nouns) 추출
nouns = okt.nouns(text)

# 4. 불필요한 단어 제거 (Stopwords)
stopwords = ['책', '이', '그', '것', '수', '저', '도', '때', '곳', '알', '나', '내']
filtered_nouns = []
for noun in nouns:
    if len(noun) > 1 and noun not in stopwords: # 1글자 단어 및 불용어 제외
        filtered_nouns.append(noun)

# 5. 단어 빈도수 계산
count = Counter(filtered_nouns)

# 6. 가장 많이 나온 상위 50개 단어 출력
print("--- 키워드 빈도수 TOP 50 ---")
print(count.most_common(50))
