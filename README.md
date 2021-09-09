# PyFi 데이터 분석 프로젝트
Python으로 하는 Financial 데이터 분석!

저희가 한 프로젝트를 소개해드리겠습니다. 😎

<hr>

# 배경
저희가 이 프로젝트를 진행한 이유는 다음과 같습니다.
> > 코로나 시국이라 사람들이 바깥에 나가지 못하며, 어떠한 것에 큰 재미를 느끼지 못하고 있습니다.
> > 
> > 그 와중에 가장 크게 관심을 가진 것이 바로 **주식**입니다.
> > 
> > 하지만 주식 초보자들은 **언제 팔아야하고 사는지 잘 모르기 때문에**
> > 
> > 도움을 주고자 주가를 **분석 및 예측**하였습니다.

<hr>

# 분석인원 소개

> Yun-bin Cho
> > 프로젝트 총괄, 모듈 제작(크롤러, 워드클라우드, 유사도, 지수평활법 예측), 프로젝트에 필요한 API 소개
> 
> Soong-ji Kim
> > 전체적인 통계 분석 시나리오 구상 및 계산, ARIMA, Prophet을 통해 데이터 예측, Plotly 그래프 작성, 크롤링 작업과 불용어 정리 참여
>
> Gi-woong Park
> > 발표 시나리오 구상, hover를 이용한 주가와 이미지 합성 그래프 시각화, 포함어와 불용어 정리
>
> Hyo-jun Kim
> > 포함어와 불용어 정리, 주가 관련 소재 찾기, 프로젝트 프로세스 병행

<hr>

# 기술스택
사용한 기술스택들은 다음과 같습니다.

> 주언어 및 개발환경
> >파이썬 (Pycharm, 실행 테스트는 Jupyter Lab)
>
> 분석용 API 및 라이브러리
> 
> > Financial Data Reader (주가 데이터 불러오기)
> > Numpy, Pandas, Plotly, Matplotlib, Scikit-Learn
>
> 보조언어 : R (지수평활 시각화를 위해 사용)

<hr>

# 감성 분석 (WordCloud 이용)
먼저 저희는 사람들의 반응이 주가에 영향을 준다고 생각하였습니다.

그래서 사람들의 반응이 가장 잘 반영되는 분야인 **엔터테인먼트**에서도 **하이브**라는 종목을 선택하였습니다.

그리고 유명 커뮤니티 사이트인 **인스티즈**에서 대중의 반응을 텍스트로 수집하였습니다.

![image](https://user-images.githubusercontent.com/59231602/132647794-aac578f4-2666-4ed4-9dbe-916cfba6fab5.png)

![image](https://user-images.githubusercontent.com/59231602/132648160-89e298c6-3967-4476-9896-94a99497b2cd.png)

먼저 인스티즈의 게시글들을 **하이브의 주가등락이 컸던 날 ±5일을 기준으로** 반응들을 불러왔습니다.
![image](https://user-images.githubusercontent.com/59231602/132648375-06525632-fc74-4f63-bb4e-3a83d6d8a7ca.png)

# 유사도 분석

# 예측
