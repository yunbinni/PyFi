""" 모듈 불러오기 """
import numpy as np
import pandas as pd
import FinanceDataReader as fdr

########################################################################################################################
""" 주가데이터 불러오기 """

# 종목코드 관련 파일 불러오기
code_KOSPI = pd.read_csv('KOSPI_20210903.csv', encoding='euc-kr').iloc[:, [0, 1]]
code_KOSDAQ = pd.read_csv('KOSDAQ_20210903.csv', encoding='euc-kr').iloc[:, [0, 1]]
code = pd.DataFrame(pd.concat([code_KOSPI, code_KOSDAQ], axis=0))
code.index = np.arange(0, code.shape[0])

# 종목코드 대신 이름으로 조회가능하게 만든 함수
def Name_to_Code(name:str) -> str:
    idx = code[code['종목명'] == name].index[0] # 해당 종목의 인덱스로 찾는다.
    return code['종목코드'][idx]

########################################################################################################################
""" 파일로 저장하는 코드 """
def writeDF(stock_Name: str, sDate: str, eDate: str) -> None:
    pd.DataFrame(fdr.DataReader(Name_to_Code(stock_Name), sDate, eDate)).to_csv(stock_Name + '_'+sDate + '-'+eDate  + '.csv', sep=',')

########################################################################################################################
""" 구동 """
if __name__ == "__main__":
    writeDF('셀트리온제약', '2021-07-01', '2021-07-31')