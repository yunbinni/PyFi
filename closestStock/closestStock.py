########################################################################################################################
""" 모듈 불러오기 """
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler

import sys
from dtw import dtw
import FinanceDataReader as fdr # 주가 데이터 불러오기
from warnings import filterwarnings ; filterwarnings('ignore') # 짜증나는 경고는 무시 ~ ^^

# 종목코드 불러오기
code_KOSPI = pd.read_csv('KOSPI_20210903.csv', encoding='euc-kr').iloc[:, [0, 1]]
code_KOSDAQ = pd.read_csv('KOSDAQ_20210903.csv', encoding='euc-kr').iloc[:, [0, 1]]
code = pd.DataFrame(pd.concat([code_KOSPI, code_KOSDAQ], axis=0))
code.index = np.arange(0, code.shape[0])

########################################################################################################################
""" 함수 정의 부분 """
# 종목코드 대신 종목이름으로 조회하게끔 해주는 함수
def Name_to_Code(name:str) -> str:
    idx = code[code['종목명'] == name].index[0] # 해당 종목의 인덱스로 찾는다.
    return code['종목코드'][idx]


# 기준종목과 비교종목간의 상관계수를 구하는 함수
def calcCorrCoef(std_Stock_Name: str, cmp_Stock_name: str, sDate: str, eDate: str) -> int:
    stdDf = pd.DataFrame(fdr.DataReader(Name_to_Code(std_Stock_Name), sDate, eDate)['Close']) # 기준종목 종가
    stdDf_Diff = pd.DataFrame(np.log(stdDf).diff(1).diff(1)[2:])

    cmpDf = pd.DataFrame(fdr.DataReader(Name_to_Code(cmp_Stock_name), sDate, eDate)['Close']) # 비교종목 종가
    cmpDf_Diff = pd.DataFrame(np.log(cmpDf).diff(1).diff(1)[2:])

    joinedDf = stdDf_Diff.join(cmpDf_Diff, lsuffix='_caller', rsuffix='_other')

    return np.corrcoef(joinedDf.iloc[:, 0], joinedDf.iloc[:, 1])[0][1]


# 기준종목과 가장 비슷한(1에 가까운) 종목 구하기
def similarStock_CorrCoef(std_Stock_Name: str, sDate: str, eDate: str) -> (int, str):
    stdDf = pd.DataFrame(fdr.DataReader(Name_to_Code(std_Stock_Name), sDate, eDate)['Close'])  # 기준종목 종가
    stdDf_Diff = pd.DataFrame(np.log(stdDf).diff(1).diff(1)[2:])                               # 차분은 2번~

    minimam = 9999
    res_StkName = ''    # 반환할 종목명
    res_Pcc = 0         # 반환활 상관계수

    # 상관계수 구하기
    for i in range(code.shape[0]):
        cmpStkCode = code.iloc[i, 0]  # 비교종목코드
        cmpStkName = code.iloc[i, 1]  # 비교종목이름

        if std_Stock_Name == cmpStkName : continue # 자기 자신과 비교하는 것 방지

        cmpDf = pd.DataFrame(fdr.DataReader(Name_to_Code(cmpStkName), sDate, eDate)['Close'])  # 비교종목 DF
        cmpDf_Diff = pd.DataFrame(np.log(cmpDf).diff(1).diff(1)[2:])

        joinedDf = stdDf_Diff.join(cmpDf_Diff, lsuffix='_caller', rsuffix='_other')

        pcc = np.corrcoef(joinedDf.iloc[:, 0], joinedDf.iloc[:, 1])[0][1]                               # 차분들의 상관계수

        # 기준데이터(1)와 가까운지?
        cmp = 1 - np.abs(pcc)

        if minimam > cmp:
            minimam = cmp
            res_StkName = cmpStkName
            res_Pcc = pcc

        print(f'StockName: {cmpStkName}, pcc: {pcc}')

    return (res_StkName, res_Pcc)


# 기준종목과 비교종목간의 dtw를 구하는 함수
def calcDTW(std_Stock_Name: str, cmp_Stock_name: str, sDate: str, eDate: str) -> int:
    stdDf = pd.DataFrame(fdr.DataReader(Name_to_Code(std_Stock_Name), sDate, eDate)['Close']) # 기준종목 종가
    cmpDf = pd.DataFrame(fdr.DataReader(Name_to_Code(cmp_Stock_name), sDate, eDate)['Close']) # 비교종목 종가

    joinedDf = stdDf.join(cmpDf, lsuffix='_caller', rsuffix='_other')

    scaler = MinMaxScaler()
    scaler.fit(joinedDf)

    data = pd.DataFrame(scaler.transform(joinedDf))

    dtw(data.iloc[:, 0], data.iloc[:, 1]).distance

    return dtw(data.iloc[:, 0], data.iloc[:, 1]).distance


# 기준종목과 가장 비슷한(0에 가까운) 종목 구하기
def similarStock_DTW(std_Stock_Name: str, sDate: str, eDate: str) -> (int, str):
    stdDf = pd.DataFrame(fdr.DataReader(Name_to_Code(std_Stock_Name), sDate, eDate)['Close'])  # 기준종목 종가

    minimam = sys.maxsize
    res_StkName = ''    # 반환할 종목명
    res_DTW = 0         # 반환활 상관계수

    # 상관계수 구하기
    for i in range(code.shape[0]):
        cmpStkCode = code.iloc[i, 0]  # 비교종목코드
        cmpStkName = code.iloc[i, 1]  # 비교종목이름

        if std_Stock_Name == cmpStkName : continue # 자기 자신과 비교하는 것 방지

        cmpDf = pd.DataFrame(fdr.DataReader(Name_to_Code(cmpStkName), sDate, eDate)['Close'])  # 비교종목 DF

        joinedDf = stdDf.join(cmpDf, lsuffix='_caller', rsuffix='_other')

        scaler = MinMaxScaler()
        scaler.fit(joinedDf)

        data = pd.DataFrame(scaler.transform(joinedDf))

        try:
            DTW = dtw(data.iloc[:, 0], data.iloc[:, 1]).distance

            if minimam > DTW:
                minimam = DTW
                res_StkName = cmpStkName
                res_DTW = DTW

        except:
            continue

        finally:
            print(f'StockName: {cmpStkName}, DTW: {DTW}')

    return (res_StkName, res_DTW)

########################################################################################################################
""" 구동 """
if __name__ == "__main__":
    print(calcDTW('셀트리온', '셀트리온헬스케어', '2021-07-08', '2021-09-07'))