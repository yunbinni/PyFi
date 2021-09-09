""" 모듈 불러오기 """
import numpy as np
import pandas as pd

# 언어관련 모듈
import konlpy
from konlpy.tag import Okt  # 구 twitter
from konlpy.tag import Kkma

from ckonlpy.tag import Twitter # 사용자 커스터마이징
from nltk import FreqDist

# 시각화, 전처리 관련
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt

# 경고 무시하기
from warnings import filterwarnings
filterwarnings('ignore')

########################################################################################################################
""" 함수 작성 부분 """

""" 워드 클라우드 생성기 (Feat.데이터 전처리) """
def createWC(inwords_Filename: str, stwords_Filename: str, data_Filename: str) -> None:
    twitter = Twitter() # 불러오기

    # 포함단어 불러오기
    with open(inwords_Filename, 'r') as f:
        inwords = f.readlines()

    inwords = [i.replace('\n', '') for i in inwords]  # 줄바꿈 기호 없애기

    # 제외단어 불러오기
    with open(stwords_Filename, 'r') as f:
        stwords = f.readlines()

    stwords = [i.replace('\n', '') for i in stwords] # 줄바꿈 기호 없애기

    # 데이터 파일 불러오기
    with open(data_Filename, 'r') as f:
        docs = f.read()

    # 단어 사전등록
    for i in inwords:
        twitter.add_dictionary(i, "Noun")

    # 명사 추출
    data = twitter.nouns(docs)

    # 한 글자 단어 제외하지만 포함단어는 포함하기
    data = [i for i in data if i in inwords or len(i) > 1]

    # 불용어 제거
    data = [i for i in data if i not in stwords]

    # 단어 빈도표 생성
    wc = FreqDist(data)

    # 워드클라우드 생성
    wcimg = WordCloud(background_color='white',
                      font_path=r'/usr/share/fonts/nanum/NanumMyeongjo.ttf',
                      random_state=42,
                      width=640, height=480).generate_from_frequencies(wc)
    plt.imshow(wcimg, interpolation='bilinear')
    plt.axis('off')
    plt.show()