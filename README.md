# 프로젝트 설명
CryptoPilot은 [upbit](https://upbit.com/exchange?code=CRIX.UPBIT.KRW-BTC)의 API를 활용하여 머신러닝 및 지표 분석을 기반으로한 비트코인 자동 트레이딩 프로그램입니다. 이 프로그램은 예측모델을 활용하여 추후의 값, 또는 추세를 예측하고 이를 기반으로 트레이딩 결정을 자동화 합니다. 여러 방식으로 학습을 시도해 보았고, 예측 모델 뿐 아니라 지표를 통한 자동 매매 또한 시도해보았습니다.

# 프로젝트 구조
- CryptoAI
    - 입력에 사용될 OHLCV 데이터를 불러와 전처리
    - 전처리된 데이터를 통해 모델으로부터 예측값을 받음
- Runner
    - 매매 로직 제작에 도움을 주는 Investor, Logger 클래스
- TradeEngine
    - 전반적인 매매 로직
    - RSI, EMA 지표 계산

# 시도했던 학습 방법들

## 모델 구조만 변경

- 에포크, 배치사이즈, 인풋의 시퀀스 길이 등을 변경했었음
- 모델 구조는 레이어 구조 뿐 아니라 활성화함수, 옵티마이저, loss function 등을 변경했음
![최초모델](https://github.com/1000zoo/CryptoPilot/assets/8938679/fade0eac-f575-4664-90fd-87c343a8fea8)

## 입출력 변경

### 최대 수익률과 최저 수익률을 아웃풋으로 학습
![다음ohlcv의최대및최저수익률](https://github.com/1000zoo/CryptoPilot/assets/8938679/44a088cf-5d92-4c09-8993-fa40f40b454d)


### 학습 데이터의 상승 하락 횡보를 로직으로 분류하여 출력으로 예측하게 학습
![카테고리컬결과](https://github.com/1000zoo/CryptoPilot/assets/8938679/a6296fd2-1d4d-476e-9d6f-def6b88306c5)

### Time Embedded를 적용하여, 하루를 주기로 1분씩 나눠 sin, cos값을 입력에 추가
![타임임베디드](https://github.com/1000zoo/CryptoPilot/assets/8938679/701ac2fa-6172-4815-bb1b-7586a1b92512)


### 그 외
- 아웃풋으로 연속된 5개의 종가를 예측하게 학습
- 아웃풋으로 OHLCV 모두 예측하게 학습


## RSI 지표 이용

- 14일 RSI를 계산하여 매매 지표로 활용
- RSI 값 30, 70을 기준으로 매매 로직 작성

# 사용 라이브러리 및 환경

- Python 3.9 이상
- tensorflow
- pyupbit
- scikit-learn
- numpy
- pandas
